#!/usr/bin/env python3

# dev/py/xlattice_py/testUStats.py

import os
import unittest
from rnglib import SimpleRNG
from xlattice.crypto import SP


class TestUStats (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG()

    def testUStats(self):
        pass

if __name__ == '__main__':
    unittest.main()
