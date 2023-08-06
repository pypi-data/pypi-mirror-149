# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
"""Run package command tests."""
import argparse

from a28.package import generate_jsondata
from tests.conftest import Helpers


def test_a28_package_no_param(helpers: Helpers) -> None:
    """Ensure all subcommands are present."""
    command = ['package']
    expect = 'usage: a28 package [-h] {init,meta,build,install,publish} ...'

    output, raise_type, exit_code = helpers.execute_error(command)

    assert raise_type == SystemExit
    assert exit_code == 2
    assert output[0:len(expect)] == expect


def test_a28_init_no_param(helpers: Helpers) -> None:
    """Test package initialization without parameters."""
    command = ['package', 'init']
    expect = 'usage: a28 package init [-h] -s SCOPE -n NAME -t'

    output, raise_type, exit_code = helpers.execute_error(command)

    assert raise_type == SystemExit
    assert exit_code == 2
    assert output[0:len(expect)] == expect


def test_a28_build_no_param(helpers: Helpers) -> None:
    """Test package build without parameters."""
    command = ['package', 'build']
    expect = 'usage: a28 package build [-h] --src SRC [--dest DEST]'

    output, raise_type, exit_code = helpers.execute_error(command)

    assert raise_type == SystemExit
    assert exit_code == 2
    assert output[0:len(expect)] == expect


def test_a28_install_no_param(helpers: Helpers) -> None:
    """Test package install without parameters."""
    command = ['package', 'install']
    expect = 'usage: a28 package install [-h] --pkg PKG'

    output, raise_type, exit_code = helpers.execute_error(command)

    assert raise_type == SystemExit
    assert exit_code == 2
    assert output[0:len(expect)] == expect


def test_generate_jsondata_without_args():
    """Check the json data generated is correct."""
    result = generate_jsondata(
        scope='foo',
        name='bar',
        identifier='1234',
        schema='234',
        args=argparse.Namespace(bin='', script=''),
    )

    assert result == {
        'description': '234 package created using A28 cmd by foo.',
        'identifier': '1234',
        'name': '@foo/bar',
        'version': '0.1.0',
    }


def test_generate_jsondata_with_bin():
    """Check the json data generated is correct with binary dir."""
    result = generate_jsondata(
        scope='foo',
        name='bar',
        identifier='1234',
        schema='234',
        args=argparse.Namespace(bin='in the bin', script=''),
    )

    assert result == {
        'description': '234 package created using A28 cmd by foo.',
        'identifier': '1234',
        'name': '@foo/bar',
        'version': '0.1.0',
        'bin': {},
    }


def test_generate_jsondata_with_bin_and_script():
    """Check the json data generated is correct with script and bin."""
    result = generate_jsondata(
        scope='foo',
        name='bar',
        identifier='1234',
        schema='234',
        args=argparse.Namespace(bin='in the bin', script='the script'),
    )

    assert result == {
        'description': '234 package created using A28 cmd by foo.',
        'identifier': '1234',
        'name': '@foo/bar',
        'version': '0.1.0',
        'bin': {},
        'scripts': {},
    }
