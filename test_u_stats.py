#!/usr/bin/env python3
# dev/py/xlattice_py/testUStats.py

""" Exercise statistical functions for content-keyed store. """

import os
import sys
import unittest
from rnglib import SimpleRNG
from xlattice import Q
from xlattice.stats import UStats
from xlattice.u import UDir


class TestUStats (unittest.TestCase):
    """ Exercise statistical functions for content-keyed store. """

    def setUp(self):
        self.rng = SimpleRNG()

    def test_defaults(self):
        s = UStats()

        self.assertEqual(s.dirStruc, UDir.DIR_FLAT)
        self.assertFalse(s.usingSHA)

        self.assertEqual(s.subDirCount, 0)
        self.assertEqual(s.subSubDirCount, 0)
        self.assertEqual(s.leafCount, 0)
        self.assertEqual(s.oddCount, 0)
        self.assertEqual(s.hasL, False)
        self.assertEqual(s.hasNodeID, False)
        self.assertEqual(s.minLeafBytes, sys.maxsize)
        self.assertEqual(s.maxLeafBytes, 0)

        self.assertEqual(len(s.unexpectedAtTop), 0)

    def test_properties(self):
        s = UStats()

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
