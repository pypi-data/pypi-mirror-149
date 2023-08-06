# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
"""Test standard command line arguments."""
from a28 import __version__
from tests.conftest import Helpers


def test_a28_no_param(helpers: Helpers) -> None:
    """Test the CLI without any parameters."""
    command = []
    expect = (
        'usage: a28 [-h] [-v]'
        ' {api,package,pkg,system,sys,account,acc} ...'
    )

    output, raise_type, exit_code = helpers.execute_error(command)

    assert raise_type == SystemExit
    assert exit_code == 2
    assert output[0:len(expect)] == expect


def test_a28_version_param(helpers: Helpers) -> None:
    """Check the correct version number is returned."""
    command = ['-v']
    expect = f'a28 version {__version__}'

    output, raise_type, exit_code = helpers.execute(command)

    assert raise_type == SystemExit
    assert exit_code == 0
    assert output[0:len(expect)] == expect


def test_a28_system_exit_on_exception(helpers: Helpers) -> None:
    """Test an exeception being raised.

    Command line call that fail would trigger a system exit with code
    other than 0.
    """
    command = ['account', 'authenticate', '-u', 'joe@example.com', '-p', '234']
    _, raise_type, exit_code = helpers.execute_error(command)

    assert raise_type == SystemExit
    assert exit_code == 1
