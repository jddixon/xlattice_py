#!/usr/bin/env python3

# dev/py/xlattice_py/testUStats.py

import os
import sys
import unittest
from rnglib import SimpleRNG
from xlattice.stats import UStats


class TestUStats (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG()

    def testDefaults(self):
        s = UStats()

        self.assertEqual(s.subDirCount, 0)
        self.assertEqual(s.subSubDirCount, 0)
        self.assertEqual(s.leafCount, 0)
        self.assertEqual(s.oddCount, 0)
        self.assertEqual(s.hasL, False)
        self.assertEqual(s.hasNodeID, False)
        self.assertEqual(s.minLeafBytes, sys.maxsize)
        self.assertEqual(s.maxLeafBytes, 0)

    def testProperties(self):
        s = UStats()

        s.subDirCount += 7
        self.assertEqual(s.subDirCount, 7)

        s.subSubDirCount += 13
        self.assertEqual(s.subSubDirCount, 13)

        s.leafCount += 31
        self.assertEqual(s.leafCount, 31)

        s.oddCount += 19
        self.assertEqual(s.oddCount, 19)

        s.hasL = True
        self.assertEqual(s.hasL, True)

        s.hasNodeID = True
        self.assertEqual(s.hasNodeID, True)

        # this value only decreases ---------------------------------
        s.minLeafBytes = 47
        self.assertEqual(s.minLeafBytes, 47)

        s.minLeafBytes = 52
        self.assertEqual(s.minLeafBytes, 47)

        s.minLeafBytes = 12
        self.assertEqual(s.minLeafBytes, 12)

        # this value only increases ---------------------------------
        s.maxLeafBytes = 47
        self.assertEqual(s.maxLeafBytes, 47)

        s.maxLeafBytes = 12
        self.assertEqual(s.maxLeafBytes, 47)

        s.maxLeafBytes = 52
        self.assertEqual(s.maxLeafBytes, 52)

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
