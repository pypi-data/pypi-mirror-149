# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
"""Test all account actions."""
import contextlib
import os
import tempfile
import unittest
from argparse import Namespace
from importlib import reload
from io import StringIO

import responses

from a28 import account, config, utils
from a28.api import ApiError
from a28.config import ConfigFile


class TestAccountMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.test_dir = tempfile.TemporaryDirectory()
        utils.CONFIG_PATH = self.test_dir.name
        utils.CONFIG = os.path.join(utils.CONFIG_PATH, 'config.json')

        reload(config)

        self.responses = responses.RequestsMock()
        self.responses.start()

        self.temp_stdout = StringIO()

        self.addCleanup(self.responses.stop)
        self.addCleanup(self.responses.reset)

    def tearDown(self) -> None:
        self.test_dir.cleanup()

    def test_authenticate_with_valid_response(self):
        self.responses.add(
            responses.GET,
            'https://assets.a28.io/plugin/endpoints.json',
            json={
                "international": {
                    "api": {
                        "endpoint": "https://api.example.com/v1"
                    }
                }
            },
            status=200
        )

        self.responses.add(
            responses.POST,
            'https://api.example.com/v1/account/signin',
            json={
                "statusCode": 200,
                "status": "SUCCESS",
                "token": "supersecrettoken11"
            },
            status=200
        )
        self.assertEqual({}, ConfigFile.load())

        with contextlib.redirect_stdout(self.temp_stdout):
            account.authenticate(
                region="international",
                email="joe@example.com",
                password="123"
            )
        output = self.temp_stdout.getvalue().strip()
        self.assertEqual("authentication successful", output)
        self.assertEqual(
            {
                'international': {
                    'email': 'joe@example.com',
                    'token': 'supersecrettoken11'
                }
            },
            ConfigFile.load()
        )

    def test_authenticate_with_param_password(self):
        self.responses.add(
            responses.GET,
            'https://assets.a28.io/plugin/endpoints.json',
            json={
                "international": {
                    "api": {
                        "endpoint": "https://api.example.com/v1"
                    }
                }
            },
            status=200
        )

        self.responses.add(
            responses.POST,
            'https://api.example.com/v1/account/signin',
            json={
                "statusCode": 200,
                "status": "SUCCESS",
                "token": "supersecrettoken11"
            },
            status=200
        )
        self.assertEqual({}, ConfigFile.load())

        with contextlib.redirect_stdout(self.temp_stdout):
            account.authenticate_interactive(
                Namespace(
                    endpoint="international",
                    email="joe@example.com",
                    password="123"
                )
            )

        self.assertEqual((
            'Warning: Using a password on the command line interface'
            ' can be insecure.\nauthentication successful'
        ),
            self.temp_stdout.getvalue().strip()
        )
        self.assertEqual(
            {
                'international': {
                    'email': 'joe@example.com',
                    'token': 'supersecrettoken11'
                }
            },
            ConfigFile.load()
        )

    def test_authenticate_with_unauthorized_response(self):
        self.responses.add(
            responses.GET,
            'https://assets.a28.io/plugin/endpoints.json',
            json={
                "international": {
                    "api": {
                        "endpoint": "https://api.example.com/v1"
                    }
                }
            },
            status=200
        )

        self.responses.add(
            responses.POST,
            'https://api.example.com/v1/account/signin',
            json={
                "statusCode": 402,
                "status": "ERROR",
                "message": "you can't"
            },
            status=402
        )
        self.assertEqual({}, ConfigFile.load())

        with self.assertRaises(ApiError):
            with contextlib.redirect_stdout(self.temp_stdout):
                account.authenticate(
                    region="international",
                    email="joe@example.com",
                    password="123"
                )

        output = self.temp_stdout.getvalue().strip()
        self.assertEqual("error authenticating: you can't", output)
        self.assertEqual({}, ConfigFile.load())

    def test_authenticate_with_failed_response(self):
        self.responses.add(
            responses.GET,
            'https://assets.a28.io/plugin/endpoints.json',
            json={
                "international": {
                    "api": {
                        "endpoint": "https://api.example.com/v1"
                    }
                }
            },
            status=200
        )

        self.responses.add(
            responses.POST,
            'https://api.example.com/v1/account/signin',
            json={},
            status=500
        )
        self.assertEqual({}, ConfigFile.load())

        with self.assertRaises(ApiError):
            with contextlib.redirect_stdout(self.temp_stdout):
                account.authenticate(
                    region="international",
                    email="joe@example.com",
                    password="123"
                )

        output = self.temp_stdout.getvalue().strip()
        self.assertEqual("error authenticating: 500", output)
        self.assertEqual({}, ConfigFile.load())
