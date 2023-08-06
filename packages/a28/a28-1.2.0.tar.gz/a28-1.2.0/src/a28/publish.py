"""Manage publication of packages."""
import logging
from argparse import Namespace, _SubParsersAction
from typing import Union

from a28 import utils
from a28.api import API, ApiError, JwtAuth
from a28.build import extract_meta
from a28.config import ConfigFile

logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
log = logging.getLogger(__name__)


def add_publish_parser(parser: _SubParsersAction):
    """Create the CLI parser for 'publish' command."""
    parser.set_defaults(func=publish)
    parser.add_argument(
        '--pkg',
        required=True,
        help='package a28 package file',
    )
    parser.add_argument(
        '-e',
        '--endpoint',
        default=API.DEFAULT_ENDPOINT,
        help='endpoint to use.',
    )


def publish(args: Namespace):
    """Call the API to publish the version."""
    publish_version(args.endpoint, args.pkg)


def publish_version(region: str, path: str) -> None:
    """Publish a new version of the given a28 package file.

    1- We'll parse the .a28 zip file to retrieve package id/version.
    2- Generate a S3 signed URL.
    3- Upload the .a28 file on S3.
    4- Then create the version using the API.
    """
    log.debug(f'publishing a version: {{"region": {region}, "path": {path}}}')

    utils.message('Uploading', end='', flush=True)

    api = API(region)

    try:
        token = ConfigFile.get_token(api.region)
        meta_data = extract_meta(path)
        utils.message('.', end='', flush=True)
        file_name = _upload_a28_file(api, token, path)
        utils.message('.', end='', flush=True)
        api.post(
            f'/package/{meta_data["identifier"]}/version',
            json_payload={
                'package': file_name,
                'version': meta_data['version']
            },
            auth=JwtAuth(token)
        )
        utils.message('.', end='', flush=True)
    except Exception as error:
        utils.message(f'\nFailed: {error}')
        raise

    utils.message('\nDone!')


def _upload_a28_file(api: API, token: str, path: str) -> Union[None, str]:
    signed_url_response = api.post(
        '/asset/generate',
        json_payload={
            'extension': 'a28',
        },
        auth=JwtAuth(token)
    )

    with open(path, 'rb') as package:
        upload_response = api.session.put(
            url=signed_url_response['data']['url'],
            data=package
        )

    if upload_response.status_code != 200:
        raise ApiError(upload_response.status_code)

    return signed_url_response['data']['name']
