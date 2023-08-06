"""Everything to interact with the A28 API."""
import json
import logging
from argparse import Namespace, _SubParsersAction
from enum import Enum
from typing import Any, Callable, Dict, Union

import certifi
import requests
from requests import Response
from requests.auth import AuthBase

from a28 import utils
from a28.config import ConfigFile

logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
log = logging.getLogger(__name__)


# can be updated to StrEnum when we are on Python 3.10
# https://docs.python.org/3.11/howto/enum.html#strenum
class ApiStatus(str, Enum):
    """Possible response of the API status field."""

    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'


class ApiError(Exception):
    """Custom exception for API errors."""

    pass


def parse_api_errors(
    response: Dict[str, Any],
    http_status_code: int
) -> Dict[str, Any]:
    """Raise error if API returned errors or invalid data."""
    if response.get('status') == ApiStatus.SUCCESS:
        return response

    if response.get('message'):
        raise ApiError(response.get('message'))

    raise ApiError(http_status_code)


def handle_api_errors(api_call) -> Callable:
    """Handle API error with a decorator."""

    def wrapper(*arg, **kwargs) -> Dict[str, Any]:
        """Process api response.

        check for errors and raise ApiError if any.
        """
        try:
            response = api_call(*arg, **kwargs)
            response_payload = json.loads(response.content)

            return parse_api_errors(response_payload, response.status_code)
        except json.JSONDecodeError as err:
            raise ApiError(f'Unknown Error: {err}')

    return wrapper


class JwtAuth(AuthBase):
    """Attaches JWT Authentication to the given Request object."""

    def __init__(self, token):
        """Create an Auth object for the requests."""
        self.token = token

    def __call__(self, request):
        """Insert the token in the Authorization header."""
        request.headers['Authorization'] = f'Bearer {self.token}'
        return request


class API:
    """Handles all the actions to the API.

    A region must be given to each instance so we can request to the
    correct API (international, china, etc..).
    """

    ENDPOINTS_URL = 'https://assets.a28.io/plugin/endpoints.json'
    DEFAULT_ENDPOINT = 'international'

    def __init__(self, region: str):
        """Initialize the API."""
        self.region = region
        self.session = requests.Session()
        self.session.verify = certifi.where()

        api_endpoints = self.fetch_endpoints()
        try:
            self.api_endpoint = api_endpoints[self.region]['api']['endpoint']
        except KeyError:
            utils.message('invalid endpoint')
            raise

        self.session.hooks['response'].append(self._check_token)

    @handle_api_errors
    def get(self, url: str, **kwargs) -> Response:
        """Send a GET request."""
        url = f'{self.api_endpoint}{url}'
        kwargs.setdefault('allow_redirects', True)
        return self.session.request('GET', url, **kwargs)

    @handle_api_errors
    def post(
        self,
        url: str,
        data=None,
        json_payload=None,
        **kwargs
    ) -> Response:
        """Send a POST request."""
        return self.session.request(
            'POST',
            self.api_endpoint + url,
            data=data,
            json=json_payload,
            **kwargs
        )

    @handle_api_errors
    def put(self, url: str, data=None, **kwargs) -> Response:
        """Send a PUT request."""
        endpoint = f'{self.api_endpoint}{url}'
        return self.session.request('PUT', endpoint, data=data, **kwargs)

    @handle_api_errors
    def patch(self, url: str, data=None, **kwargs) -> Response:
        """Send a PATCH request."""
        endpoint = f'{self.api_endpoint}{url}'
        return self.session.request('PATCH', endpoint, data=data, **kwargs)

    @handle_api_errors
    def delete(self, url: str, **kwargs) -> Response:
        """Send a DELETE request."""
        endpoint = f'{self.api_endpoint}{url}'
        return self.session.request('DELETE', endpoint, **kwargs)

    def _check_token(self, response: Response, *_args, **_kwargs) -> None:
        """
        Update the local token to a token returned by a server.

        When a server responds to a request, the server can return a
        newly updated token. The new token could be in response to new
        information stored within the token, or the token age might be
        getting close to the expiry time and a token refresh is needed.
        For more information on bearer tokens, please refer to
        `bearer tokens <https://datatracker.ietf.org/doc/html/rfc6750>`.

        This method checks if a updated token has been returned and
        stores it in the preferences system for future requests if the
        token is valid.

        This function is called as a requests hook.
        """
        try:
            json_data = response.json()
        except json.JSONDecodeError:
            return

        if 'token' not in json_data:
            return

        with ConfigFile() as data:
            if self.region not in data:
                data[self.region] = {}
            data[self.region]['token'] = json_data['token']

    def fetch_endpoints(self) -> Dict[str, Any]:
        """Fetch the Area28 endpoint list.

        Returns the decoded JSON to the calling method.
        """
        req = self.session.get(self.ENDPOINTS_URL, allow_redirects=True)
        try:
            regions = json.loads(req.content)
            regions['dev'] = {'api': {'endpoint': 'https://dev-api.a28.io/v1'}}
            return regions
        except json.JSONDecodeError as error:
            utils.message(f'error decoding endpoints: {error}')
            raise


def get_package(region: str, identifier: str) -> Union[Dict[str, Any], None]:
    """Retrieve a package from the API."""
    response = f'{{"region": {region}, "identifier": {identifier}}}'
    log.debug(f'retrieving package: {response}')

    api = API(region)
    config = ConfigFile.load()

    try:
        response = api.get(
            f'/package/{identifier}',
            auth=JwtAuth(config[api.region]['token'])
        )

        return response.get('data')
    except ApiError as error:
        utils.message(f'unable to get package: {error}')
        raise


def register_package(
    region: str,
    scope: str,
    name: str,
    schema: str
) -> Union[str, None]:
    """Create a package with the API and returns the new uuid."""
    log.debug(f'creating package: {{"region": {region}, "name": {name}}}')

    api = API(region)
    config = ConfigFile.load()

    try:
        response = api.post(
            f'/group/{scope}/package',
            json_payload={
                'name': name,
                'type': schema,
            },
            auth=JwtAuth(config[api.region]['token'])
        )

        return response['data']['identifier']
    except ApiError as error:
        utils.message(f'unable to create package: {error}')
        raise


def status(args: Namespace) -> None:
    """Display the status of an endpoint.

    Submit an options request to an api endpoint to check if the
    endpoint returns a 200 or a 304 status response message with a JSON
    payload that has a status response and a StatusCode set.
    """
    api = API(args.endpoint)
    try:
        response = api.get('/status')
        utils.message(response['message'])
    except (ApiError, KeyError):
        utils.message('unable to connect to endpoint')
        raise


def endpoints(_args: Namespace) -> None:
    """Fetch and print the endpoints."""
    api = API(API.DEFAULT_ENDPOINT)

    for endpoint in api.fetch_endpoints():
        utils.message(endpoint)


def find_or_create_package(
    region: str,
    schema: Union[str, None] = None,
    scope: Union[str, None] = None,
    name: Union[str, None] = None,
    identifier: Union[str, None] = None,
) -> Union[str, None]:
    """Find or create a package and returns its UUID.

    if an identifier is provided we'll retrieve it from the API.
    Else we'll create it.
    """
    if identifier:
        existing_package = get_package(region, identifier)

        if not existing_package:
            return

        return existing_package.get('identifier')

    return register_package(
        region=region,
        schema=schema,
        scope=scope,
        name=name,
    )


def cli_options(main_parser: _SubParsersAction) -> None:
    """Argument for the API subcommand."""
    parser = main_parser.add_parser(
        'api',
        help='api actions'
    )
    api_parser = parser.add_subparsers(
        dest='api',
        required=True,
        help='api',
    )
    parser_endpoints = api_parser.add_parser(
        'endpoints',
        help='list all endpoints.',
    )
    parser_endpoints.set_defaults(func=endpoints)
    parser_status = api_parser.add_parser(
        'status',
        help='show the status of an endpoint.',
    )
    parser_status.add_argument(
        '-e',
        '--endpoint',
        required=True,
        help='the name of the endpoint to check the status of.',
    )
    parser_status.set_defaults(func=status)
