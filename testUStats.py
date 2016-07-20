#!/usr/bin/env python3

# dev/py/xlattice_py/testUStats.py

import os
import sys
import unittest
from rnglib import SimpleRNG
from xlattice.stats import UStats
from xlattice.u import DIR_FLAT


class TestUStats (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG()

    def testDefaults(self):
        s = UStats()

        self.assertEqual(s.dirStruc, DIR_FLAT)
        self.assertEqual(s.usingSHA1, False)

        self.assertEqual(s.subDirCount, 0)
        self.assertEqual(s.subSubDirCount, 0)
        self.assertEqual(s.leafCount, 0)
        self.assertEqual(s.oddCount, 0)
        self.assertEqual(s.hasL, False)
        self.assertEqual(s.hasNodeID, False)
        self.assertEqual(s.minLeafBytes, sys.maxsize)
        self.assertEqual(s.maxLeafBytes, 0)

        self.assertEqual(len(s.unexpectedAtTop), 0)

    def testProperties(self):
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
