#!/usr/bin/env python3
"""Test all the pattoo modules."""

from __future__ import print_function
import os
import inspect
import re
import sys
import collections


# Try to create a working PYTHONPATH
DEV_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(DEV_DIR, os.pardir)), os.pardir))
if DEV_DIR.endswith('/pattoo/tests/bin') is True:
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/bin" directory. \
Please fix.''')
    sys.exit(2)


# Import pattoo libraries
from pattoo_shared import errors


def main():
    """Get all the error codes used in pattoo.

    Args:
        None

    Returns:
        None

    """
    # Get code report
    minimum = 20000
    maximum = 39999    
    errors.check_source_code(ROOT_DIR, minimum=minimum, maximum=maximum)


if __name__ == '__main__':
    main()
