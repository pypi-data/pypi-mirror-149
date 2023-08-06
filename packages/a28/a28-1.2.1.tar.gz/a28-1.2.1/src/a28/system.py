"""Manage actions relating to the system running area28.

The actions provided by the system module adds the ability to manage the
state of the computer system running Area28 allowing for developers to
maintain the configuration and paths of the system.
"""
import os
import shutil
from argparse import Namespace, _SubParsersAction

from a28 import utils


def cli_options(mainparser: _SubParsersAction) -> None:
    """System subcommand arguments.

    Define the arguments that the system subcommand can accept. The
    system subcommand supports the following commands:

    clean: Clean all files from the current system.
    exists: Return if the system currently contains a configuration.
    path: Return the current system configuration path.
    """
    parser = mainparser.add_parser(
        'system',
        aliases=['sys'],
        help='system actions'
    )
    subparser = parser.add_subparsers(
        dest='system',
        required=True,
        help='system',
    )
    env_group = parser.add_mutually_exclusive_group(required=True)
    env_group.add_argument(
        '--environment', "-e",
        dest='environment',
        required=False,
        default='dev',
        choices=['prod', 'staging', 'dev'],
        help='switch the environment to use'
    )
    env_group.add_argument(
        '--all', "-a",
        required=False,
        action='store_true',
        help='remove all environments'
    )
    parser_exist = subparser.add_parser(
        'exists',
        help='check if the system configuration exists.',
    )
    parser_exist.set_defaults(func=exists)
    parser_clean = subparser.add_parser(
        'clean',
        help='clean (delete) the configuration permanently.',
    )
    parser_clean.set_defaults(func=clean)
    parser_clean.add_argument(
        '-f',
        '--force',
        action='store_true',
        help='force the configuration to be removed bypassing confirmation',
    )
    parser_path = subparser.add_parser(
        'path',
        help='return the location of the configuration path.',
    )
    parser_path.set_defaults(func=path)
    parser_path.add_argument(
        '-m',
        '--minimal',
        action='store_true',
        help='return a minimal version of the path to use in scripts',
    )


def clean_at_path(config_path: str, force_remove: bool = False) -> None:
    """Clean all the config files relating to Area28.

    Using the shutil utilities, delete all the files provided in the
    config_path directory. If an error occurs, catch the exception and
    print it out to the STDOUT.

    Args:
        args (Namespace): The list of provided arguments.

    Returns:
        None: Does not return any value.
    """
    message = f'Delete ALL configuration data from "{config_path}"? y/n?'

    if not force_remove and not utils.confirm(message):
        utils.message(f'Not deleting {config_path}')
        return

    # else the user wants to delete the config at the specified path
    if not os.path.isdir(config_path):
        utils.message(f'No configuration to clean at "{config_path}".')
        raise FileNotFoundError

    try:
        shutil.rmtree(config_path)
        utils.message(f'Deleted all files and directories in {config_path}')
    except OSError as e:
        utils.message(f'Error: {config_path} : {e.strerror}')
        raise


def clean(args: Namespace) -> None:
    """Clean all the configuration files relating to Area28.

    Using the shutil utilities,
    if all is specified, ask and delete all the env [prod, dev, stagin]
    accordingly, or else, remove all the files provided in the args.path
    directory. If an error occurs, catch the exception and print it out
    to the STDOUT.

    Args:
        args (Namespace): The list of provided arguments.

    Returns:
        None: Does not return any value.
    """
    environment = args.environment if not args.all else ''
    environment_path = os.path.join(utils.STORAGE, environment)
    clean_at_path(environment_path, force_remove=args.force)


def exists(args: Namespace) -> None:
    """Check if the configuration directory exists.

    Using the path provided in the arguments, check if the configuration
    path exists. If no path is provided, the default path defined in the
    system utility is used.

    Args:
        args (Namespace): The list of provided arguments.

    Returns:
        None: Does not return any value.
    """
    environment = args.environment if not args.all else ''
    environment_path = os.path.join(utils.STORAGE, environment)
    if os.path.isdir(environment_path):
        utils.message(f'Configuration exists at "{environment_path}".')
    else:
        utils.message(f'No configuration exists at "{environment_path}".')


def path(args: Namespace) -> None:
    """Print the path of the system configuration.

    Print the path currently used to store the system configuration
    files. If the path option is provided in the ArgParse Namespace, the
    provided path will be returned.

    If the minimal ArgParse namespace is provided and set to boolean
    True, the output will be reduced to only the path.

    It does NOT change the configuration path

    Args:
        args (Namespace): The list of provided arguments.

    Returns:
        None: Does not return any value.
    """
    environment = args.environment if not args.all else ''
    environment_path = os.path.join(utils.STORAGE, environment)
    if args.minimal:
        utils.message(f'{environment_path}')
    else:
        utils.message(f'Configuration path set to "{environment_path}".')
