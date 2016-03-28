#!/usr/bin/python3

# dev/py/xlattice_py/testCrypto.py

import os
import unittest
from rnglib import SimpleRNG
from xlattice.crypto import SP


class TestCrypto (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG()

    def testSpaces(self):
        for i in range(4):
            j = self.rng.nextInt16(32)
            spaces = SP.getSpaces(j)
            self.assertEqual(len(spaces), j)
            for k in range(len(spaces)):
                self.assertEqual(spaces[k], ' ')

if __name__ == '__main__':
    unittest.main()
