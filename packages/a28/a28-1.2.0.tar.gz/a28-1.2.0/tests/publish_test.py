# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
"""Test publishing an application."""
import contextlib
import os
import tempfile
import unittest
from argparse import Namespace
from io import StringIO

import responses
from responses import matchers

from a28 import config, utils
from a28.api import ApiError
from a28.config import ConfigFile
from a28.publish import publish


class TestPublishMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.TemporaryDirectory()
        utils.CONFIG_PATH = self.test_dir.name
        utils.CONFIG = os.path.join(utils.CONFIG_PATH, 'config.json')

        self.responses = responses.RequestsMock()
        self.responses.start()

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

        with ConfigFile() as data:
            data['international'] = {
                'email': 'joe@example.com',
                'token': 'supersecrettoken11'
            }

        package = '814a3feb-e9b2-4a5f-9088-4b108b47b0e9-6.6.6.a28'
        self.temp_stdout = StringIO()
        self.test_file_path = f'{os.path.dirname(__file__)}/fixtures/{package}'

        self.addCleanup(self.responses.stop)
        self.addCleanup(self.responses.reset)

    def tearDown(self) -> None:
        self.test_dir.cleanup()

    def test_successful_version_publish(self):
        self.responses.add(
            responses.POST,
            'https://api.example.com/v1/asset/generate',
            json={
                "statusCode": 200,
                "status": "SUCCESS",
                "data": {
                    "url": 'https://fakes3.example.com/bucket/uploadme',
                    "name": 'package-6.6.6.a28'
                }
            },
            status=200,
            match=[matchers.json_params_matcher({
                "extension": "a28"
            })]
        )

        self.responses.add(
            responses.PUT,
            'https://fakes3.example.com/bucket/uploadme',
            status=200
        )

        package = '814a3feb-e9b2-4a5f-9088-4b108b47b0e9'
        self.responses.add(
            responses.POST,
            f'https://api.example.com/v1/package/{package}/version',
            json={
                "statusCode": 201,
                "status": "SUCCESS"
            },
            status=201,
            match=[matchers.json_params_matcher({
                'package': 'package-6.6.6.a28',
                'version': '6.6.6'
            })]
        )

        with contextlib.redirect_stdout(self.temp_stdout):
            publish(Namespace(
                endpoint='international',
                pkg=self.test_file_path,
            ))

        output = self.temp_stdout.getvalue().strip()
        self.assertEqual("Uploading...\nDone!", output)

    def test_version_publish_not_auth(self):
        os.remove(utils.CONFIG)

        with self.assertRaises(config.ConfigError):
            with contextlib.redirect_stdout(self.temp_stdout):
                publish(Namespace(
                    endpoint='international',
                    pkg=self.test_file_path,
                ))

        self.assertEqual(
            "Uploading\nFailed: please authenticate",
            self.temp_stdout.getvalue().strip(),
        )

    def test_version_publish_fail_to_find_file(self):

        with self.assertRaises(FileNotFoundError):
            with contextlib.redirect_stdout(self.temp_stdout):
                publish(Namespace(
                    endpoint='international',
                    pkg='./fixtures/dontexist.a28',
                ))

        no_file = '[Errno 2] No such file or directory:'
        self.assertEqual(
            f"Uploading\nFailed: {no_file} './fixtures/dontexist.a28'",
            self.temp_stdout.getvalue().strip(),
        )

    def test_version_publish_fail_generate_upload_url(self):
        self.responses.add(
            responses.POST,
            'https://api.example.com/v1/asset/generate',
            json={
                "statusCode": 402,
                "status": "ERROR",
                "message": "I don't like you"
            },
            status=402
        )

        with self.assertRaises(ApiError):
            with contextlib.redirect_stdout(self.temp_stdout):
                publish(Namespace(
                    endpoint='international',
                    pkg=self.test_file_path,
                ))

        self.assertEqual(
            "Uploading.\nFailed: I don't like you",
            self.temp_stdout.getvalue().strip(),
        )

    def test_version_publish_fail_upload_to_s3(self):
        self.responses.add(
            responses.POST,
            'https://api.example.com/v1/asset/generate',
            json={
                "statusCode": 200,
                "status": "SUCCESS",
                "data": {
                    "url": 'https://fakes3.example.com/bucket/uploadme',
                    "name": 'package-6.6.6.a28'
                }
            },
            status=200
        )

        self.responses.add(
            responses.PUT,
            'https://fakes3.example.com/bucket/uploadme',
            status=500
        )

        with self.assertRaises(ApiError):
            with contextlib.redirect_stdout(self.temp_stdout):
                publish(Namespace(
                    endpoint='international',
                    pkg=self.test_file_path,
                ))

        self.assertEqual(
            "Uploading.\nFailed: 500",
            self.temp_stdout.getvalue().strip(),
        )

    def test_version_publish_fail_create_version(self):
        self.responses.add(
            responses.POST,
            'https://api.example.com/v1/asset/generate',
            json={
                "statusCode": 200,
                "status": "SUCCESS",
                "data": {
                    "url": 'https://fakes3.example.com/bucket/uploadme',
                    "name": 'package-6.6.6.a28'
                }
            },
            status=200
        )

        self.responses.add(
            responses.PUT,
            'https://fakes3.example.com/bucket/uploadme',
            status=200
        )

        package = '814a3feb-e9b2-4a5f-9088-4b108b47b0e9'
        self.responses.add(
            responses.POST,
            f'https://api.example.com/v1/package/{package}/version',
            json={
                "statusCode": 409,
                "status": "ERROR",
                "message": "version already exists"
            },
            status=409
        )

        with self.assertRaises(ApiError):
            with contextlib.redirect_stdout(self.temp_stdout):
                publish(Namespace(
                    endpoint='international',
                    pkg=self.test_file_path,
                ))

        self.assertEqual(
            "Uploading..\nFailed: version already exists",
            self.temp_stdout.getvalue().strip(),
        )
