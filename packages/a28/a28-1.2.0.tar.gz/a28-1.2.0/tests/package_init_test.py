# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
"""Test package initialization."""
import contextlib
import json
import os
import tempfile
import unittest
from argparse import Namespace
from importlib import reload
from io import StringIO

import responses

from a28 import config, package, utils
from a28.api import ApiError
from a28.config import ConfigFile


class TestPackageInitMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.TemporaryDirectory()
        utils.CONFIG_PATH = self.test_dir.name
        utils.CONFIG = os.path.join(utils.CONFIG_PATH, 'config.json')

        reload(config)

        self.responses = responses.RequestsMock()
        self.responses.start()

        self.temp_stdout = StringIO()

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

        self.addCleanup(self.responses.stop)
        self.addCleanup(self.responses.reset)

    def tearDown(self) -> None:
        self.test_dir.cleanup()

    def test_successful_package_init(self):
        self.responses.add(
            responses.POST,
            'https://api.example.com/v1/group/nicescopegroup/package',
            json={
                "statusCode": 201,
                "status": "SUCCESS",
                "data": {
                    "identifier": '1234567'
                }
            },
            status=201
        )

        with contextlib.redirect_stdout(self.temp_stdout):
            package.initialize(
                Namespace(
                    bin=None,
                    script=None,
                    identifier=None,
                    endpoint='international',
                    path=self.test_dir.name,
                    name='nicetest',
                    scope='nicescopegroup',
                    type='app',
                )
            )
        output = self.temp_stdout.getvalue().strip()
        self.assertEqual("package created", output)

        description = 'app package created using A28 cmd by nicescopegroup.'
        with open(f'{self.test_dir.name}/package.json') as json_file:
            data = json.load(json_file)
            self.assertEqual(
                {
                    'description': description,
                    'identifier': '1234567',
                    'name': '@nicescopegroup/nicetest',
                    'version': '0.1.0'
                },
                data
            )

    def test_package_init_with_error(self):
        self.responses.add(
            responses.POST,
            'https://api.example.com/v1/group/nicescopegroup/package',
            json={
                "statusCode": 500,
                "status": "ERROR",
                "message": "server crashed again"
            },
            status=500
        )

        with self.assertRaises(ApiError):
            with contextlib.redirect_stdout(self.temp_stdout):
                package.initialize(
                    Namespace(
                        bin=None,
                        script=None,
                        identifier=None,
                        endpoint='international',
                        path=self.test_dir.name,
                        name='nicetest',
                        scope='nicescopegroup',
                        type='app',
                    )
                )

        self.assertEqual(
            "unable to create package: server crashed again",
            self.temp_stdout.getvalue().strip()
        )
        is_file = os.path.isfile(f'{self.test_dir.name}/package.json')
        self.assertEqual(False, is_file)

    def test_successful_package_init_on_new_folder(self):
        self.responses.add(
            responses.POST,
            'https://api.example.com/v1/group/nicescopegroup/package',
            json={
                "statusCode": 201,
                "status": "SUCCESS",
                "data": {
                    "identifier": 'imagreeatuuid'
                }
            },
            status=201
        )

        with contextlib.redirect_stdout(self.temp_stdout):
            package.initialize(
                Namespace(
                    bin=None,
                    script=None,
                    identifier=None,
                    endpoint='international',
                    path=f'{self.test_dir.name}/newfolder',
                    name='nicetest',
                    scope='nicescopegroup',
                    type='app',
                )
            )

        output = self.temp_stdout.getvalue().strip()
        self.assertEqual("package created", output)

        description = 'app package created using A28 cmd by nicescopegroup.'
        with open(f'{self.test_dir.name}/newfolder/package.json') as json_file:
            data = json.load(json_file)
            self.assertEqual(
                {
                    'description': description,
                    'identifier': 'imagreeatuuid',
                    'name': '@nicescopegroup/nicetest',
                    'version': '0.1.0'
                },
                data
            )

    def test_package_init_with_no_config(self):
        os.remove(utils.CONFIG)

        with self.assertRaises(SystemExit) as err:
            with contextlib.redirect_stdout(self.temp_stdout):
                package.initialize(
                    Namespace(
                        bin=None,
                        script=None,
                        identifier=None,
                        endpoint='international',
                        path=self.test_dir.name,
                        name='nicetest',
                        scope='nicescopegroup',
                        type='app',
                    )
                )

        self.assertEqual(err.exception.code, 1)
        self.assertEqual(
            "authenticate before initializing",
            self.temp_stdout.getvalue().strip()
        )
        is_file = os.path.isfile(f'{self.test_dir.name}/package.json')
        self.assertEqual(False, is_file)

    def test_successful_package_init_with_existing_uuid(self):
        self.responses.add(
            responses.GET,
            'https://api.example.com/v1/package/existinguuid11',
            json={
                "statusCode": 200,
                "status": "SUCCESS",
                "data": {
                    "identifier": 'existinguuid11'
                }
            },
            status=200
        )

        with contextlib.redirect_stdout(self.temp_stdout):
            package.initialize(
                Namespace(
                    bin=None,
                    script=None,
                    identifier='existinguuid11',
                    endpoint='international',
                    path=self.test_dir.name,
                    name='nicetest',
                    scope='nicescopegroup',
                    type='app',
                )
            )
        output = self.temp_stdout.getvalue().strip()
        self.assertEqual("package created", output)

        description = 'app package created using A28 cmd by nicescopegroup.'
        with open(f'{self.test_dir.name}/package.json') as json_file:
            data = json.load(json_file)
            self.assertEqual(
                {
                    'description': description,
                    'identifier': 'existinguuid11',
                    'name': '@nicescopegroup/nicetest',
                    'version': '0.1.0'
                },
                data
            )

    def test_unsuccessful_package_init_with_existing_uuid(self):
        self.responses.add(
            responses.GET,
            'https://api.example.com/v1/package/existinguuid21',
            json={
                "statusCode": 404,
                "status": "ERROR",
                "message": "DOES NOT EXIST"
            },
            status=404
        )

        with self.assertRaises(ApiError):
            with contextlib.redirect_stdout(self.temp_stdout):
                package.initialize(
                    Namespace(
                        bin=None,
                        script=None,
                        identifier='existinguuid21',
                        endpoint='international',
                        path=self.test_dir.name,
                        name='nicetest',
                        scope='nicescopegroup',
                        type='app',
                    )
                )

        self.assertEqual(
            "unable to get package: DOES NOT EXIST",
            self.temp_stdout.getvalue().strip()
        )
        is_file = os.path.isfile(f'{self.test_dir.name}/package.json')
        self.assertEqual(False, is_file)
