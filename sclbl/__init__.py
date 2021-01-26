"""
The sclbl package provide CLI tools for the Scailable Platform
"""
import sys

from .cli import *
from .version import __version__

# Check python version
if sys.version_info < (3, 0):
    print('sclbl requires Python 3, while Python ' + str(sys.version[0] + ' was detected. Terminating... '))
    sys.exit(1)

