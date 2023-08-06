"""Build packages to be submitted to Area28."""
import argparse
import sys

from a28 import __version__, account, api, package, system


def build_parser():
    """Build the argument for the cli."""
    parser = argparse.ArgumentParser(
        'a28',
        description='Area28 development kit'
    )
    app = '%(prog)s version ' + __version__
    parser.add_argument('-v', '--version', action='version', version=app)
    sub = parser.add_subparsers(dest='action', required=True, help='actions')

    api.cli_options(sub)
    package.cli_options(sub)
    system.cli_options(sub)
    account.cli_options(sub)

    return parser


def main(args=None):
    """Command line entry point."""
    args = args or sys.argv[1:]
    parser = build_parser()

    try:
        args = parser.parse_args(args)
        args.func(args)
        raise SystemExit(0)

    except Exception:
        sys.exit(1)
