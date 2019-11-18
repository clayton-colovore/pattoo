#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
import time

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                os.path.abspath(os.path.join(
                        EXEC_DIR,
                        os.pardir)), os.pardir)), os.pardir)), os.pardir))

if EXEC_DIR.endswith(
        '/pattoo/tests/test_pattoo/ingest/db') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo/ingest/db" \
directory. Please fix.''')
    sys.exit(2)

from pattoo_shared import data
from pattoo_shared.constants import DATA_FLOAT
from tests.libraries.configuration import UnittestConfig
from pattoo.ingest.db import query, insert, exists


class TestBasicFunctioins(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_checksum(self):
        """Testing method / function checksum."""
        # Initialize key variables
        result = exists.checksum(-1)
        self.assertFalse(result)

        # Create entry and check
        checksum = data.hashstring(str(int(time.time())))
        result = exists.checksum(checksum)
        self.assertFalse(result)
        insert.checksum(checksum, DATA_FLOAT)
        result = exists.checksum(checksum)
        self.assertTrue(result)

    def test_pair(self):
        """Testing method / function pair."""
        pass

    def test_glue(self):
        """Testing method / function glue."""
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
