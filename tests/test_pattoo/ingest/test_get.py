#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
from random import random

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
                EXEC_DIR, os.pardir)), os.pardir)), os.pardir))

if EXEC_DIR.endswith(
        '/pattoo/tests/test_pattoo/ingest') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo/tests/test_pattoo/ingest" \
directory. Please fix.''')
    sys.exit(2)

from pattoo_shared import data
from pattoo_shared.constants import DATA_FLOAT, PattooDBrecord
from tests.libraries.configuration import UnittestConfig
from pattoo.ingest.db import query, insert, exists
from pattoo.ingest import get


class TestBasicFunctioins(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_pairs(self):
        """Testing method / function pairs."""
        pair1 = ('key1', data.hashstring(str(random())))
        pair2 = ('key2', data.hashstring(str(random())))

        # Create a PattooDBrecord
        record = PattooDBrecord(
            checksum='1',
            data_index='2',
            data_label='3',
            data_source=4,
            data_timestamp=5,
            data_type=DATA_FLOAT,
            data_value=6,
            metadata=[pair1, pair2]
        )

        # Pairs shouldn't exist
        self.assertFalse(exists.pair(pair1[0], pair1[1]))
        self.assertFalse(exists.pair(pair2[0], pair2[1]))

        # Insert items
        result = get.pairs(record)
        self.assertTrue(exists.pair(pair1[0], pair1[1]))
        self.assertTrue(exists.pair(pair2[0], pair2[1]))
        self.assertTrue(exists.pair(pair1[0], pair1[1]) in result)
        self.assertTrue(exists.pair(pair2[0], pair2[1]) in result)

    def test_key_value_pairs(self):
        """Testing method / function key_value_pairs."""
        # Create a PattooDBrecord
        record = PattooDBrecord(
            checksum='1',
            data_index='2',
            data_label='3',
            data_source=4,
            data_timestamp=5,
            data_type=DATA_FLOAT,
            data_value=6,
            metadata=[('key1', 'value'), ('key2', 'value')])

        # Test
        expected = [
            ('data_index', '2'), ('data_label', '3'), ('data_source', '4'),
            ('data_type', '101'), ('key1', 'value'), ('key2', 'value')
        ]
        result = get.key_value_pairs(record)
        self.assertEqual(sorted(result), expected)

        # Test with a list
        result = get.key_value_pairs([record])
        self.assertEqual(result, expected)

    def test_idx_checksum(self):
        """Testing method / function idx_checksum."""
        # Initialize key variables
        checksum = data.hashstring(str(random()))
        self.assertFalse(exists.checksum(checksum))

        # Test creation
        result = get.idx_checksum(checksum, DATA_FLOAT)
        expected = exists.checksum(checksum)
        self.assertEqual(result, expected)

        # Test after creation
        result = get.idx_checksum(checksum, DATA_FLOAT)
        expected = exists.checksum(checksum)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
