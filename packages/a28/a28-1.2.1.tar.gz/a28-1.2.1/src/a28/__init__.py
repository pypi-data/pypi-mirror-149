"""Build packages to be submitted to Area28."""
import logging

import coloredlogs

# current version
__version__ = '1.2.1'

# enable logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
coloredlogs.install(level='DEBUG', logger=log)
