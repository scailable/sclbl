"""
The sclbl package provide CLI tools for the Scailable Platform
"""
# Ran on import of the package. Check version:
import sys

if sys.version_info < (3, 0):
    print('sclbl requires Python 3, while Python ' + str(sys.version[0] + ' was detected. Terminating... '))
    sys.exit(1)