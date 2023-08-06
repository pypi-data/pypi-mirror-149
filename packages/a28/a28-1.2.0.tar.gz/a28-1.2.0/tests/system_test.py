# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
"""Test system commands."""
from pathlib import Path

from tests.conftest import Helpers


def test_a28_system_no_param(helpers: Helpers) -> None:
    """Test execution of system sub argument without parameters."""
    command = ['system']
    expect = 'usage: a28 system [-h] (--environment {prod,staging,dev}'

    output, raise_type, exit_code = helpers.execute_error(command)

    assert raise_type == SystemExit
    assert exit_code == 2
    assert output[0:len(expect)] == expect


def test_a28_exists_no_param_no_config(helpers: Helpers, tmp_path: Path):
    """Test execution of system exists without config."""
    command = ['system', '-a', 'exists']
    config_path = tmp_path / 'config_path'
    expect = f'No configuration exists at "{config_path}/".'
    output, raise_type, exit_code = helpers.execute(command, config_path)

    assert raise_type == SystemExit
    assert exit_code == 0
    assert expect == output


def test_a28_exists_no_param_config(helpers: Helpers, tmp_path: Path) -> None:
    """Test execution of system sub argument without parameters."""
    command = ['system', '-a', 'exists']
    config_path = tmp_path / 'config_path'
    expect = f'Configuration exists at "{config_path}/".'
    config_path.mkdir()
    output, raise_type, exit_code = helpers.execute(command, config_path)

    assert raise_type == SystemExit
    assert exit_code == 0
    assert expect == output


def test_a28_clean_no_param_no_config(helpers: Helpers, tmp_path: Path):
    """Test execution of system clean without config."""
    command = ['system', '-a', 'clean', '-f']
    config_path = tmp_path / 'config_path'
    expect = f'No configuration to clean at "{config_path}/".'
    output, raise_type, exit_code = helpers.execute(command, config_path)

    assert raise_type == SystemExit
    assert exit_code == 1
    assert expect == output


def test_a28_clean_no_param_config(helpers: Helpers, tmp_path: Path) -> None:
    """Test execution of system sub argument without parameters."""
    command = ['system', '-a', 'clean', '-f']
    config_path = tmp_path / 'config_path'
    expect = f'Deleted all files and directories in {config_path}/'
    config_path.mkdir()
    output, raise_type, exit_code = helpers.execute(command, config_path)

    assert raise_type == SystemExit
    assert exit_code == 0
    assert expect == output


def test_a28_path_minimal_dev(helpers: Helpers, tmp_path: Path) -> None:
    """Test execution of system sub argument without parameters."""
    command = ['system', '-e=dev', 'path', '--minimal']
    expect = tmp_path / 'dev'

    output, raise_type, exit_code = helpers.execute(command, tmp_path)

    assert raise_type == SystemExit
    assert exit_code == 0
    assert expect.resolve() == Path(output).resolve()


def test_a28_path_minimal_prod(helpers: Helpers, tmp_path: Path) -> None:
    """Test execution of system sub argument without parameters."""
    command = ['system', '-e=prod', 'path', '--minimal']
    expect = tmp_path / 'prod'

    output, raise_type, exit_code = helpers.execute(command, tmp_path)

    assert raise_type == SystemExit
    assert exit_code == 0
    assert expect.resolve() == Path(output).resolve()


def test_a28_path_minimal_all(helpers: Helpers, tmp_path: Path) -> None:
    """Test execution of system sub argument with all parameter."""
    command = ['system', '--all', 'path', '--minimal']
    expect = tmp_path

    output, raise_type, exit_code = helpers.execute(command, tmp_path)

    assert raise_type == SystemExit
    assert exit_code == 0
    assert expect.resolve() == Path(output).resolve()


def test_a28_path_no_minimal(helpers: Helpers, tmp_path: Path) -> None:
    """Test execution of system sub argument without minimal."""
    command = ['system', '--all', 'path']
    expect = f'Configuration path set to "{tmp_path.resolve()}/".'
    output, raise_type, exit_code = helpers.execute(command, tmp_path)

    assert raise_type == SystemExit
    assert exit_code == 0
    assert expect == output
