"""Create build of a package."""
import json
import os
import zipfile
from argparse import _SubParsersAction

from a28 import utils

PKG_FILE = 'package.json'


def add_build_parser(parser: _SubParsersAction):
    """Create the CLI parser for 'build' command."""
    parser.set_defaults(func=build)
    parser.add_argument(
        '--src',
        required=True,
        help='package source directory',
    )
    parser.add_argument(
        '--dest',
        default='',
        help='destination directory',
    )


def build(args):
    """Build package."""
    src = args.src
    dest = args.dest
    meta = get_info(src)
    pkg = package(src, dest, meta)
    utils.message(pkg)


def package(src, dest, meta):
    """Build an a28 package from the provided src directory.

    The package will be saved to the dest directory. A package needs to
    be provided containing at least an identifier and a version number.
    """
    version = meta['version']
    identifier = meta['identifier']
    filename = '{}-{}.{}'.format(identifier, version, 'a28')
    filename = os.path.join(dest, filename)

    os.makedirs(dest, exist_ok=True)

    a28 = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    exclude = (['build', '.vscode', '.git', '.github', 'dist'])
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in exclude]
        for current in files:
            i_file = os.path.join(root, current)
            fl = os.path.relpath(
                os.path.join(root, current),
                os.path.join(src),
            )
            a28.write(i_file, fl)
    a28.close()
    return filename


def get_info(src, extracted=False):
    """Get information about a package.

    Using the package.json file located within the packages directory,
    fetch the information about the package including the version number
    and identifier.
    """
    if extracted:
        data = json.load(src)
    else:
        package_config = os.path.join(src, PKG_FILE)
        with open(package_config) as package_data:
            data = json.load(package_data)
    return data


def extract_meta(pkg):
    """Extract the meta information from a packaged package."""
    with zipfile.ZipFile(pkg) as zf:
        package_config = next(x for x in zf.namelist() if x.endswith(PKG_FILE))
        with zf.open(package_config) as index:
            return get_info(index, True)
