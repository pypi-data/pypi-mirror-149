"""Manage package creation, building, and submitting.

The package module provides a set of utilities designed for package
developers to create packages, build packages from python source code,
and submit packages to be included in the list of installable packages
within Area28.
"""
import hashlib
import json
import os
import shutil
from argparse import Namespace

from a28 import log, utils
from a28.api import API, find_or_create_package
from a28.build import add_build_parser, extract_meta
from a28.config import ConfigFile
from a28.publish import add_publish_parser

package_types = [
    'api',
    'app',
    'chat',
    'event',
    'interface',
    'logger',
    'metadata',
    'preference',
    'realtime',
    'repository',
    'ui',
    'units',
]


def cli_options(main_parser):
    """Argparse options added to the cli."""
    parser = main_parser.add_parser(
        'package',
        aliases=['pkg'],
        help='package actions'
    )
    package_parser = parser.add_subparsers(
        dest='package',
        required=True,
        help='package',
    )

    add_init_parser(
        package_parser.add_parser(
            'init',
            help='Initialize a package',
        )
    )
    add_meta_parser(
        package_parser.add_parser(
            'meta',
            help='Display package information'
        )
    )
    add_build_parser(
        package_parser.add_parser(
            'build',
            help='build package',
        )
    )
    add_install_parser(
        package_parser.add_parser(
            'install',
            help='install package',
        )
    )
    add_publish_parser(
        package_parser.add_parser(
            'publish',
            help='publish a package',
        )
    )


def add_meta_parser(parser_meta) -> None:
    """Create the meta command."""
    parser_meta.set_defaults(func=meta)
    parser_meta.add_argument(
        'path',
        default='.',
        help='package path "."'
    )


def add_init_parser(parser_init):
    """Create the CLI parser for 'init' command."""
    parser_init.set_defaults(func=initialize)
    parser_init.add_argument(
        'path',
        default='.',
        help='package path default "."',
    )
    parser_init.add_argument(
        '-s',
        '--scope',
        required=True,
        help='package scope eg. group-name',
    )
    parser_init.add_argument(
        '-n',
        '--name',
        required=True,
        help='package name eg. pkg-name',
    )
    parser_init.add_argument(
        '-t',
        '--type',
        required=True,
        choices=package_types,
        help='package type',
    )
    parser_init.add_argument(
        '-i',
        '--identifier',
        required=False,
        help='provide a pre-registered identifier (defaults to API value)',
    )
    parser_init.add_argument(
        '--bin',
        action='store_true',
        help='create the bin directory',
    )
    parser_init.add_argument(
        '--script',
        action='store_true',
        help='create the scripts directory',
    )
    parser_init.add_argument(
        '-f',
        '--force',
        action='store_true',
        help='force overwriting package.json',
    )
    parser_init.add_argument(
        '-e',
        '--endpoint',
        default=API.DEFAULT_ENDPOINT,
        help='endpoint to use.',
    )


def add_install_parser(parser_install):
    """Create the CLI parser for 'install' command."""
    parser_install.set_defaults(func=install)
    parser_install.add_argument(
        '--pkg',
        required=True,
        help='package a28 package file',
    )


def generate_sub_dirs(args):
    """Generate a list of sub directories from the give args."""
    sub_dirs = ['extensions', 'plugins']

    if args.bin:
        log.debug('adding bin')
        sub_dirs.append('bin')
    if args.script:
        log.debug('adding scripts')
        sub_dirs.append('script')
    if args.type == 'application':
        sub_dirs.append('plugin')

    return sub_dirs


def generate_jsondata(scope, name, schema, identifier, args):
    """Generate a basic package.json data."""
    json_data = {
        'name': f'@{scope}/{name}',
        'description': f'{schema} package created using A28 cmd by {scope}.',
        'version': '0.1.0',
        'identifier': identifier,
    }

    if args.bin:
        json_data['bin'] = {}
    if args.script:
        json_data['scripts'] = {}

    return json_data


def meta(args) -> None:
    """Display package meta information."""
    package = os.path.join(args.path, 'package.json')

    if not os.path.exists(package):
        utils.message(f'invalid package path {package}')

    info = get_info(args.path)
    for name, value in info.items():
        utils.message(f'{name}: {value}')


def initialize(args: Namespace):
    """Initialize a package in a specified directory."""
    (path, name, scope, schema) = _get_init_args(args)
    log.info(f'initializing @{scope}/{name} in folder "{path}"')

    # check if the user has authenticated
    if not ConfigFile.load():
        utils.message('authenticate before initializing')
        raise SystemExit(1)

    identifier = find_or_create_package(
        region=args.endpoint,
        identifier=args.identifier,
        schema=schema,
        scope=scope,
        name=name,
    )

    if not identifier:
        raise SystemExit(1)

    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    json_file = os.path.join(path, 'package.json')

    _build_structure(path, generate_sub_dirs(args))
    overwrite = 'overwrite package.json?'
    if not os.path.isfile(json_file) or args.force or utils.confirm(overwrite):
        log.info('creating package.json')
        with open(json_file, 'w') as pkg_file:
            json.dump(
                generate_jsondata(scope, name, schema, identifier, args),
                pkg_file,
                indent=4,
            )
    else:
        log.info('not overwriting package.json')
        return

    utils.message('package created')


def install(args):
    """Install / update the local package."""
    pkg_hash = generate_hash(args.pkg)
    meta = extract_meta(args.pkg)
    meta['hash'] = pkg_hash
    install_local(args.pkg, meta)
    utils.message('installed {}'.format(meta['name']))


def install_local(pkg, meta):
    """Install package locally by calling the update_index function."""
    dest = os.path.join(utils.STORAGE, 'cache')
    shutil.copy(pkg, dest)
    index = os.path.join(utils.STORAGE, 'index.json')
    with open(index, 'r+') as index_data:
        update_index(index_data, meta)


def update_index(index_data, meta):
    """Update the index.json without touching the etag.json file.

    This will be overwritten when new official index.json is published.
    """
    data = json.load(index_data)
    data['packages'][meta['name']] = meta
    if meta['name'] not in data['required']:
        data['required'].append(meta['name'])
    index_data.seek(0)
    json.dump(data, index_data, indent=4)
    index_data.truncate()


def generate_hash(pkg):
    """Generate a hash for a package."""
    sha256_hash = hashlib.sha256()
    with open(pkg, 'rb') as f:
        # read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b''):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def _get_init_args(args):
    path = os.path.realpath(args.path)
    if not utils.valid_string(args.name):
        raise ValueError(f'{args.name} is not a valid name')
    name = args.name.lower()
    if not utils.valid_string(args.scope):
        raise ValueError(f'{args.scope} is not a valid scope')
    scope = args.scope.lower()
    if not utils.valid_string(args.type, min_length=2):
        raise ValueError(f'{args.type} is not a valid name')
    schema = args.type.lower()
    return path, name, scope, schema


def _build_structure(path, subdirs):
    for subdir in subdirs:
        os.makedirs(os.path.join(path, subdir), exist_ok=True)


def get_info(src, extracted=False):
    """Get information about a package.

    Using the package.json file located within the packages directory,
    fetch the information about the package including the version number
    and identifier.
    """
    if extracted:
        data = json.load(src)
    else:
        package = os.path.join(src, 'package.json')
        with open(package) as package_data:
            data = json.load(package_data)
    return data
