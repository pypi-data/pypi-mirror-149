# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
"""Test package building."""
import contextlib
import os
import tempfile
import unittest
from argparse import Namespace
from io import StringIO

from a28.build import build


class TestAccountMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.TemporaryDirectory()
        self.temp_stdout = StringIO()
        cur_dir = os.path.dirname(__file__)
        self.test_package_path = f'{cur_dir}/fixtures/fake-pkg'

    def tearDown(self) -> None:
        self.test_dir.cleanup()

    def test_successful_build(self):
        dest_dir = self.test_dir.name
        with contextlib.redirect_stdout(self.temp_stdout):
            build(Namespace(src=self.test_package_path, dest=dest_dir))

        package = 'e3c02b90-3513-4742-81c5-fefa3abee637-0.1.0.a28'
        self.assertEqual(
            f'{self.test_dir.name}/{package}',
            self.temp_stdout.getvalue().strip()
        )

    def test_successful_build_new_folder(self):
        dest_dir = f'{self.test_dir.name}/newfolder'
        with contextlib.redirect_stdout(self.temp_stdout):
            build(Namespace(src=self.test_package_path, dest=dest_dir))

        package = 'e3c02b90-3513-4742-81c5-fefa3abee637-0.1.0.a28'
        self.assertEqual(
            f'{self.test_dir.name}/newfolder/{package}',
            self.temp_stdout.getvalue().strip()
        )
