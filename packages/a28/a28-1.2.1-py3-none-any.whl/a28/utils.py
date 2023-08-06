"""All the utils functions."""
import os
import re
import sys

# set platform currently being used and major and minor Python version
PLATFORM = sys.platform
PYTHON_MAJOR = sys.version_info.major
PYTHON_MINOR = sys.version_info.minor

# set platform type (use startswith to handle old vers with ver nums)
POSIX = os.name == 'posix'
WINDOWS = os.name == 'nt'
LINUX = sys.platform.startswith('linux')
MACOS = sys.platform.startswith('darwin')
OSX = MACOS  # deprecated alias (thanks David F for the reminder)
FREEBSD = sys.platform.startswith('freebsd')
OPENBSD = sys.platform.startswith('openbsd')
NETBSD = sys.platform.startswith('netbsd')
BSD = FREEBSD or OPENBSD or NETBSD
SUNOS = sys.platform.startswith(('sunos', 'solaris'))
AIX = sys.platform.startswith('aix')

# get the users home path for storing files
if POSIX:
    HOMEDIR = os.path.expanduser('~')
elif WINDOWS:
    HOMEDIR = os.environ['APPDATA']
else:
    # unsupported operating system
    HOMEDIR = os.path.realpath(os.sep)

# set the storage constant
if MACOS:
    APP_SUP = os.path.join(HOMEDIR, 'Library', 'Application Support')
    STORAGE = os.path.join(APP_SUP, 'Area28', 'core')
elif WINDOWS:
    STORAGE = os.path.join(HOMEDIR, 'Area28', 'core')
elif POSIX:
    STORAGE = os.path.join(HOMEDIR, '.config', 'area28', 'core')
else:
    STORAGE = os.path.join(HOMEDIR, '.area28', 'core')

# set the devkit configuration location
CONFIG_PATH = os.path.realpath(os.path.join(STORAGE, os.pardir, 'devkit'))
CONFIG = os.path.join(CONFIG_PATH, 'config.json')


def message(msg='', flush=False, sep=' ', end='\n'):
    """Display a message to the user."""
    print(msg, sep=sep, end=end, flush=flush)


def confirm(msg='confirm?'):
    """Ask the user to confirm their action.

    Ask the user to confirm that ALL files and directories should be
    deleted from the directory specified by the storage variable. The
    STORAGE variable changes depending on the operating system used.
    """
    return bool(
        input(msg) in (
            'y',
            'Y',
            'yes',
            'ok',
            'sure',
            'alrighty',
            'of course',
            'yup', 'oui'
        )
    )


def valid_string(value, min_length=3, max_length=64):
    """Validate string input.

    Check if a string contains only alphanumeric, hyphen, and underscore
    characters and limited to 64 characters.
    """
    check = rf'^[\w_-]{{{min_length},{max_length}}}$'
    return re.match(check, value) is not None
