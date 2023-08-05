#!/usr/bin/env python3

import os
import io
import re
import codecs
import zipfile
import argparse
import itertools
import mimetypes
from glob import glob
from urllib.parse import urljoin, urlsplit, quote
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        # self.boundary = mimetools.choose_boundary()
        self.boundary = '----------lImIt_of_THE_fIle_eW_$'
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, body))
        return

    def get_binary(self):
        """Return a binary buffer containing the form data, including attached files."""
        def to_bytes(s):
            return s.encode('ascii') if isinstance(s, str) else s

        part_boundary = '--' + self.boundary

        binary = io.BytesIO()
        needsCLRF = False
        # Add the form fields
        for name, value in self.form_fields:
            if needsCLRF:
                binary.write('\r\n')
            needsCLRF = True

            block = [part_boundary,
              'Content-Disposition: form-data; name="%s"' % name,
              '',
              value
            ]
            binary.write('\r\n'.join(block))

        # Add the files to upload
        for field_name, filename, content_type, body in self.files:
            if needsCLRF:
                binary.write('\r\n')
            needsCLRF = True

            block = [part_boundary,
              str('Content-Disposition: file; name="%s"; filename="%s"' % \
              (field_name, filename)),
              'Content-Type: %s' % content_type,
              ''
              ]
            binary.write(b'\r\n'.join([to_bytes(s) for s in block]))
            binary.write(b'\r\n')
            binary.write(to_bytes(body))

        # add closing boundary marker,
        binary.write(to_bytes('\r\n--' + self.boundary + '--\r\n'))
        return binary


def url_server_path(url):
    scheme, netloc, path, query, fragment = urlsplit(url)
    return f"{scheme}{netloc}", f"{path}{query}{fragment}"


def main():
    parser = argparse.ArgumentParser(
        prog="gitlab-release",
        description='Upload files to gitlab tag (release)',
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50, width=180)
    )
    # if os.environ.get("__DOCS__", None):


    parser.add_argument('--server', default=urljoin(os.environ.get('CI_PROJECT_URL'), '/'),
                        help='url of gitlab server (default: $CI_PROJECT_URL)')
    parser.add_argument('--project_id', default=os.environ.get('CI_PROJECT_ID'),
                        help='Unique id of project, available in '
                             'Project Settings/General (default: $CI_PROJECT_ID)')
    parser.add_argument('--release_tag', default=os.environ.get('CI_COMMIT_TAG'),
                        help='Tag to upload files against (default: $CI_COMMIT_TAG)')
    parser.add_argument('--timeout', type=int, default=120, help='Timeout for http requests')
    parser.add_argument('--ignore_cert', action="store_true", help='Ignore ssl certificate failures')

    parser.add_argument('--job-id', default=os.environ.get('CI_JOB_ID', 0), help='Override the job number used for artifacts')
    parser.add_argument('--artifact-zip', action="store_true", help='Link artifacts zip from current job')

    parser.add_argument('--zip', help='Add all files to provided zip name and upload that')
    parser.add_argument('--description', default='', help='Release description to be put in front of the files')
    parser.add_argument('--link-prefix', default='', help='Prefix text added in front of each file link, eg "* " to create a list')
    parser.add_argument('--link-in-desc', action="store_true", help='Add the artifact links to the description. Uses release asset otherwise')

    parser.add_argument('--link-type', default='package', help='The type of the link: other, runbook, image, package')

    parser.add_argument('--link-artifact', action="store_true", help='Link files as artifact from the current job')

    parser.add_argument('--no-registry', action="store_true", help="Don't upload artifacts to generic registry, attach to tag description instead")
    parser.add_argument('--registry-vers', help='Upload artifacts to generic registry with provided version (default tag version numbers)')
    parser.add_argument('--registry-package-name', default=os.environ.get('CI_PROJECT_NAME', ""), help='Upload artifacts to generic registry with provided version (default project name)')
    parser.add_argument('--use-api-url', action="store_true" , help='By default, urls will be regular gitlab web urls will be used in release. Set this to use api url instead.')

    parser.add_argument('--private-token', default=os.environ.get('PRIVATE_TOKEN', ""), help='login token with permissions to commit to repo')

    parser.add_argument('--create-tag', action="store_true", help="create the tag if it doesn't already exist")
    parser.add_argument('files', nargs="*", help='glob/s of files to upload')

    args = parser.parse_args()

    server = args.server
    if not server or server == '/':
        raise SystemExit("Must provide --server if not running from CI (hence without env var 'CI_PROJECT_URL')")

    project_id = args.project_id
    if not project_id:
        raise SystemExit("Must provide --project_id if not running from CI (hence without env var 'CI_PROJECT_ID')")
    project_id = quote(project_id, safe='')

    release_tag = args.release_tag
    if not release_tag:
        raise SystemExit("Must provide --release_tag if not running from CI (hence without env var 'CI_COMMIT_TAG')")

    verify = not args.ignore_cert

    print("Uploading to %s (id: %s) @ %s" % (server, project_id, release_tag))

    if not server.endswith('/'):
        server += '/'

    api_url = f"{server}api/v4/projects/{project_id}"

    link_in_desc = args.link_in_desc or args.link_prefix

    uploads = []
    assets = []

    if args.description:
        uploads.append(args.description)

    all_files = list(itertools.chain(*[glob(f.replace('\\', '/')) if '*' in f else [f] for f in args.files]))

    if not (all_files or args.artifact_zip or args.link_artifact):
        raise SystemExit("No files found for %s" % args.files)

    token = os.environ.get('CI_JOB_TOKEN')
    job_auth = {'JOB-TOKEN': token}

    private_token = args.private_token
    private_auth = {'PRIVATE-TOKEN': private_token}

    if all_files and not private_token and not token:
        if re.match(r'[A-Za-z0-9]', all_files[0]):
            print("WARNING: legacy use of PRIVATE_TOKEN as first positional argument detected or token not supplied, please see `gitlab_release --help`")
            private_token = all_files[0]
            all_files = all_files[1:]

    if all_files and private_token == all_files[0]:
        print("WARNING: legacy use of PRIVATE_TOKEN as first positional argument detected, please see `gitlab_release --help`")
        all_files = all_files[1:]

    if private_token:
        auth = private_auth
    elif token:
        auth = job_auth
        if args.no_registry and not args.link_artifact:
            raise SystemExit("File upload to tag is not available with CI_JOB_TOKEN, must use 'PRIVATE_TOKEN'")
        if args.create_tag:
            raise SystemExit("Create Tag is not available with CI_JOB_TOKEN, must use 'PRIVATE_TOKEN'")
        if link_in_desc:
            raise SystemExit("Saving the links to tag description is not available with CI_JOB_TOKEN, must use 'PRIVATE_TOKEN'")
    else:
        raise SystemExit("Neither PRIVATE_TOKEN nor CI_JOB_TOKEN available, must be in env var 'PRIVATE_TOKEN' or provided as arg with --private-token")

    artifact_job = args.job_id
    if args.artifact_zip or args.link_artifact:
        if not artifact_job:
            print("Must provide --artifact-job <id> for artifact files")
            exit(-1)

        if args.link_artifact:
            for fname in all_files:
                if fname.startswith('./'):
                    fname = fname[2:]
                url = api_url + "/jobs/%s/artifacts/%s" % (artifact_job, fname)

                if link_in_desc:
                    uploads.append(
                        "%s[%s](%s)" % (args.link_prefix, fname, url)
                    )
                else:
                    assets.append((fname, url))

        if args.artifact_zip:
            url = api_url + "/jobs/%s/artifacts" % artifact_job
            fname = "artifact.zip"  # todo find a better name automatically?

            if link_in_desc:
                uploads.append(
                    "%s[%s](%s)" % (args.link_prefix, fname, url)
                )
            else:
                assets.append((fname, url))

    if args.zip:
        with zipfile.ZipFile(args.zip, "w", zipfile.ZIP_DEFLATED) as zf:
            def zipdir(path, ziph):
                # ziph is zipfile handle
                for root, dirs, files in os.walk(path):
                    for file in files:
                        ziph.write(os.path.join(root, file))

            for fname in all_files:
                print (fname)
                if fname == args.zip:
                    continue
                if os.path.isdir(fname):
                    zipdir(fname, zf)
                else:
                    zf.write(fname)

        all_files = [os.path.abspath(args.zip)]

    # Get the base url for links
    if args.use_api_url:
        project_base_url = api_url
    else:
        # Project API - note this cannot be accessed with CI_JOB_TOKEN
        rsp = requests.get(api_url, headers=auth, verify=verify)
        try:
            rsp.raise_for_status()
        except Exception as ex:
            if private_token:
                raise SystemExit("Obtaining project info failed, check auth token: {ex}".format(ex=ex))
            project_base_url = os.environ.get("CI_PROJECT_URL", api_url)
            if project_base_url == api_url:
                print("Could not retrieve web_url, api_url will be used for links instead.")
        else:
            response = rsp.json()
            project_base_url = response['web_url']

    if all_files and not args.link_artifact:
        print("Uploading %s" % all_files)

        for fpath in all_files:

            with codecs.open(fpath, 'rb') as filehandle:
                if not args.no_registry:
                    # Upload to generic repository
                    fname = os.path.basename(fpath)
                    vers = args.registry_vers or release_tag.strip('v')
                    package_name = args.registry_package_name or os.environ.get("CI_PROJECT_TITLE")
                    if not package_name and project_base_url == api_url:
                        raise SystemExit("Could not determine project title, please set with --registry-package-name")
                    else:
                        package_name = project_base_url.split('/')[-1]

                    if not re.match(r'\A(\.?[\w\+-]+\.?)+$', vers):
                        print("WARN: --registry-vers does not match required pattern, please see: https://docs.gitlab.com/ee/user/packages/generic_packages/index.html")

                    package_url = "{api_url}/packages/generic/{package_name}/{vers}/{fname}".format(
                        api_url=api_url,
                        vers=quote(vers, safe=''),
                        package_name=quote(package_name, safe=''),
                        fname=fname,
                    )
                    rsp = requests.put(package_url, data=filehandle, headers=auth, verify=verify)
                    if rsp.status_code == 401 and private_token and token:
                        # Failed to upload with private token, retry with ci-token
                        rsp_ = requests.put(package_url, data=filehandle, headers=job_auth, verify=verify)
                        if rsp_.status_code != 401:
                            print("WARN: uploading to package registry failed with private-token, job-token used instead.")
                            rsp = rsp_

                    try:
                        rsp.raise_for_status()
                    except Exception as ex:
                        details = ""
                        try:
                            details = f"\nerror: {rsp.json()['error']}" 
                        except:
                            pass
                        if rsp.status_code == 401:
                            details += f"\nError 401 typically means PRIVATE_TOKEN used and/or the user that started this job does not have permission to access the package registry" 
                            details += f"\nFor more details see: https://docs.gitlab.com/ee/user/packages/generic_packages/#authenticate-to-the-package-registry" 
                        if rsp.status_code == 403:
                            details += f"\nError 403 typically means the package registry is disabled in project settings." 
                            details += f"\nTo check, on the gitlab project page go to 'Settings > General', Expand the 'Visibility, project features, permissions' section and check the 'Packages' feature is enabled." 
                        if rsp.status_code == 400:
                            details += f"\nError 400 typically means the version number, project or package name does not match registry restrictions."
                            details += f"\nFor more details see: https://docs.gitlab.com/ee/user/packages/generic_packages/#publish-a-package-file" 
                        raise SystemExit(f"Upload of {fname} failed: {ex}{details}")
                    else:
                        print("Uploaded:", package_url)
                        if link_in_desc:
                            uploads.append("%s[%s](%s)" % (args.link_prefix, fname, package_url))
                        else:
                            assets.append((fname, package_url))

                else:
                    # Attach file to the repo
                    upload_url = api_url + '/uploads'
                    rsp = requests.post(upload_url, files={'file': filehandle}, headers=auth, verify=verify)
                    try:
                        rsp.raise_for_status()
                    except Exception as ex:
                        raise SystemExit("Upload of {f} failed: {ex}".format(f=fname, ex=ex))
                    else:
                        response = rsp.json()
                        if link_in_desc:
                            uploads.append(
                                "%s%s" % (args.link_prefix, response['markdown'])
                            )
                        else:
                            assets.append((response['alt'], project_base_url + response['url']))

    def fix_markdown(match):
        return "[%s](%s)" % (match.group(1), quote(match.group(2), safe='/:'))

    uploads = [re.sub(r'^\[(.*)\]\((.*)\)$', fix_markdown, u) for u in uploads]

    description = '  \n'.join(uploads)

    method = requests.post
    release_exists = False

    # Now we've got the uploaded file info, attach that to the tag
    if args.create_tag or link_in_desc:
        tag_url = api_url + ('/repository/tags/{t}'.format(t=quote(release_tag, safe='')))
        try:
            tag_details = requests.get(tag_url, headers=auth, verify=verify).json()
        except Exception as ex:
            tag_details = None

        if tag_details is None or '404' in tag_details['message']:
            if args.create_tag:
                default_branch = requests.get(api_url, headers=auth, verify=verify).json().get('default_branch', 'master')
                url = api_url + '/repository/tags?tag_name={t}&ref={r}'.format(
                    t=quote(release_tag, safe=''), r=quote(default_branch, safe='')
                )
                tag_details = requests.post(url, headers=auth, verify=verify).json()
            else:
                raise SystemExit("Tag not found:", release_tag)

        if link_in_desc and 'release' in tag_details and tag_details['release'] is not None:
            print('Update existing release')
            description = '  \n'.join((tag_details['release']['description'], description))
            method = requests.put
            release_exists = True

    data = {'tag_name': release_tag, 'description': description}

    if not link_in_desc:
        rsp = requests.get(api_url + '/releases/' + quote(release_tag), headers=auth, verify=verify)
        if rsp.status_code == 200:
            release_exists = True

        data["assets"] = dict(
                links=[
                    dict(name=name, url=url, link_type=args.link_type) for name, url in assets
                ]
            )

    try:
        def add_links_to_release():
            print("Adding details to existing release")
            if link_in_desc:
                # Update the existing release description
                rsp = method(api_url + '/releases/' + quote(release_tag), data={'description': description},
                             headers=auth, verify=verify)
                rsp.raise_for_status()

            else:
                # Post as separate file links
                for link in data["assets"]['links']:
                    _rsp = requests.post(api_url + '/releases/' + quote(release_tag) + '/assets/links', headers=auth,
                                         verify=verify, data=link)
                    if _rsp.status_code == 401 and not private_token:
                        print("It appears extra asset links can't be added with CI_JOB_TOKEN still, try with PRIVATE_TOKEN")
                    _rsp.raise_for_status()

        if release_exists:
            # Add new assets
            add_links_to_release()
        else:
            # Create new release
            rsp = requests.post(api_url + '/releases', json=data, headers=auth, verify=verify)
            if rsp.status_code == 409:
                # Conflict for url - usually means release already exists but we were
                # unable to query due to CI_JOB_TOKEN permissions
                add_links_to_release()
            else:
                rsp.raise_for_status()

        print("Uploaded %s to tag %s: %s" % (all_files, release_tag, project_base_url + "/tags/%s" % quote(release_tag)))

    except Exception as ex:
        raise SystemExit("Uploading release failed: {f}, error: {ex}".format(f=all_files, ex=ex))


if __name__ == '__main__':
    main()
