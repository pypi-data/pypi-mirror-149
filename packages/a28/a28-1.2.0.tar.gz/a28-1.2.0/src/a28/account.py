"""Manage account actions.

Using the requests module, authenticate an account on the API and store
the authentication token within a local file.
"""
from argparse import Namespace, _SubParsersAction
from getpass import getpass

from a28 import utils
from a28.api import API, ApiError
from a28.config import ConfigFile


def cli_options(main_parser: _SubParsersAction) -> None:
    """Account subcommand arguments."""
    parser = main_parser.add_parser(
        'account',
        aliases=['acc'],
        help='account actions'
    )
    subparser = parser.add_subparsers(
        dest='account',
        required=True,
        help='account',
    )
    parser_authenticate = subparser.add_parser(
        'authenticate',
        help='authenticate with the endpoint.',
    )
    parser_authenticate.set_defaults(func=authenticate_interactive)
    parser_authenticate.add_argument(
        '-e',
        '--endpoint',
        default=API.DEFAULT_ENDPOINT,
        help='endpoint to use.',
    )
    parser_authenticate.add_argument(
        '-u',
        '--email',
        required=True,
        help='your email address.',
    )
    parser_authenticate.add_argument(
        '-p',
        '--password',
        help='your password.',
    )


def authenticate_interactive(args: Namespace) -> None:
    """Get the user's password."""
    if args.password:
        message = (
            'Warning: Using a password on the command line'
            ' interface can be insecure.'
        )
        utils.message(message)
        password = args.password
    else:
        password = getpass(prompt='Enter your password:')

    authenticate(args.endpoint, args.email, password)


def authenticate(region: str, email: str, password: str) -> None:
    """Authenticate to the API."""
    api = API(region)

    try:
        api.post(url='/account/signin', json_payload={
            'email': email,
            'password': password
        })

        # save the email for reference
        # token will be saved by req hook (see _check_token function)
        with ConfigFile() as data:
            data[api.region]['email'] = email

        utils.message('authentication successful')
    except ApiError as error:
        utils.message(f'error authenticating: {error}')
        raise
