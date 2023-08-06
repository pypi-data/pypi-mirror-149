# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
"""Test the a28 utilities."""
import pytest

from a28 import utils


def test_string_validation_short() -> None:
    """Test if a string is to short."""
    assert utils.valid_string('ab', min_length=3) is False


def test_string_validation_long() -> None:
    """Test if a string is to long."""
    assert utils.valid_string('abcdefghijklmnop', max_length=10) is False


def test_string_validation_invalid() -> None:
    """Test to ensure valid characters are not allowed."""
    assert utils.valid_string('!@£$%^&*(())__+') is False


def test_string_validation_valid() -> None:
    """Test a string with valid characters."""
    assert utils.valid_string('avalidword') is True


def test_confirm_nope(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test negative confirmation."""
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "nope")
    result = utils.confirm('test message')

    assert result is False


def test_confirm_y(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test positive confirmation."""
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "y")
    result = utils.confirm('test message')

    assert result is True


def test_confirm_yes(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test positive confirmation."""
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "yes")
    result = utils.confirm('test message')

    assert result is True


def test_confirm_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test positive confirmation."""
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "ok")
    result = utils.confirm('test message')

    assert result is True


def test_confirm_sure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test positive confirmation."""
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "sure")
    result = utils.confirm('test message')

    assert result is True


def test_confirm_alrighty(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test positive confirmation."""
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "alrighty")
    result = utils.confirm('test message')

    assert result is True


def test_confirm_ofcourse(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test positive confirmation."""
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "of course")
    result = utils.confirm('test message')

    assert result is True


def test_confirm_yup(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test positive confirmation."""
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "yup")
    result = utils.confirm('test message')

    assert result is True
