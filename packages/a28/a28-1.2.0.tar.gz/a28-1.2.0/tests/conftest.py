# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
"""Helper methods for testing."""
import contextlib
from io import StringIO
from pathlib import Path
from typing import List, Optional, Tuple, Type

import pytest

from a28 import utils
from a28.cli import main


class Helpers:
    """A set of helper utilities used for testing."""

    @staticmethod
    def execute_error(
        command: List[str],
        location: Optional[Path] = None
    ) -> Tuple[str, type, int]:
        """Execute the main a28 function with the provided arguments."""
        temp_stdout = StringIO()

        if location:
            utils.STORAGE = location

        with pytest.raises(SystemExit) as excinfo:
            with contextlib.redirect_stderr(temp_stdout):
                main(command)

        exit_code = excinfo.value.code
        raise_type = excinfo.type

        tmp_output = temp_stdout.getvalue().strip()
        if len(tmp_output.splitlines()):
            output = temp_stdout.getvalue().strip().splitlines()[0]
        else:
            output = tmp_output

        return output, raise_type, exit_code

    @staticmethod
    def execute(
        command: List[str],
        location: Optional[Path] = None
    ) -> Tuple[str, type, int]:
        """Execute the main a28 function with the provided arguments."""
        temp_stdout = StringIO()

        if location:
            utils.STORAGE = location

        with pytest.raises(SystemExit) as excinfo:
            with contextlib.redirect_stdout(temp_stdout):
                main(command)

        exitcode = excinfo.value.code
        raise_type = excinfo.type

        tmp_output = temp_stdout.getvalue().strip()
        if len(tmp_output.splitlines()):
            output = temp_stdout.getvalue().strip().splitlines()[0]
        else:
            output = tmp_output

        return output, raise_type, exitcode


@pytest.fixture()
def helpers() -> Type[Helpers]:
    """Return the helper methods used for testing."""
    return Helpers
