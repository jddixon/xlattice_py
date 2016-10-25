#!/usr/bin/env python3
# dev/py/xlattice_py/testUStats.py

""" Exercise statistical functions for content-keyed store. """

import os
import sys
import unittest
from rnglib import SimpleRNG
from xlattice.stats import UStats
from xlattice.u import UDir


class TestUStats(unittest.TestCase):
    """ Exercise statistical functions for content-keyed store. """

    def setUp(self):
        self.rng = SimpleRNG()

    def test_defaults(self):
        string = UStats()

        self.assertEqual(string.dir_struc, UDir.DIR_FLAT)
        self.assertFalse(string.using_sha)

        self.assertEqual(string.subdir_count, 0)
        self.assertEqual(string.sub_subdir_count, 0)
        self.assertEqual(string.leaf_count, 0)
        self.assertEqual(string.odd_count, 0)
        self.assertEqual(string.has_l, False)
        self.assertEqual(string.has_node_id, False)
        self.assertEqual(string.min_leaf_bytes, sys.maxsize)
        self.assertEqual(string.max_leaf_bytes, 0)

        self.assertEqual(len(string.unexpected_at_top), 0)

    def test_properties(self):
        string = UStats()

        # XXX STUB XXX

# subDirCount
# subSubDirCount
# leafCount
# oddCount
# hasL
# hasNodeID
# minLeafBytes
# maxLeafBytes

if __name__ == '__main__':
    unittest.main()
