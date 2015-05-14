#!/usr/bin/python3

# xlattice_py/testPKCS7.py

import base64, hashlib, os, time, unittest

from rnglib             import SimpleRNG
from xlattice.crypto    import *

class TestPKCS7Padding (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG( time.time() )
    def tearDown(self):
        pass

    # utility functions #############################################
    
    # actual unit tests #############################################
    
    def testPadding (self):

        seven = bytearray(7)
        self.rng.nextBytes(seven)

        fifteen = bytearray(15)
        self.rng.nextBytes(fifteen)

        sixteen = bytearray(16)
        self.rng.nextBytes(sixteen)

        seventeen = bytearray(17)
        self.rng.nextBytes(seventeen)

        padding = pkcs7Padding(seven, AES_BLOCK_SIZE)
        self.assertEqual(len(padding), AES_BLOCK_SIZE-7)
        self.assertEqual(padding[0], AES_BLOCK_SIZE-7)

        padding = pkcs7Padding(fifteen, AES_BLOCK_SIZE)
        self.assertEqual(len(padding), AES_BLOCK_SIZE-15)
        self.assertEqual(padding[0], AES_BLOCK_SIZE-15)

        padding = pkcs7Padding(sixteen, AES_BLOCK_SIZE)
        self.assertEqual(len(padding), AES_BLOCK_SIZE)
        self.assertEqual(padding[0], 16)

        padding = pkcs7Padding(seventeen, AES_BLOCK_SIZE)
        expectedLen = 2*AES_BLOCK_SIZE - 17
        self.assertEqual(len(padding), expectedLen)
        self.assertEqual(padding[0], expectedLen)

        paddedSeven = addPKCS7Padding(seven, AES_BLOCK_SIZE)
        unpaddedSeven = stripPKCS7Padding(paddedSeven, AES_BLOCK_SIZE)
        self.assertEqual(seven, unpaddedSeven)

        paddedFifteen = addPKCS7Padding(fifteen, AES_BLOCK_SIZE)
        unpaddedFifteen = stripPKCS7Padding(paddedFifteen, AES_BLOCK_SIZE)
        self.assertEqual(fifteen, unpaddedFifteen)

        paddedSixteen = addPKCS7Padding(sixteen, AES_BLOCK_SIZE)
        unpaddedSixteen = stripPKCS7Padding(paddedSixteen, AES_BLOCK_SIZE)
        self.assertEqual(sixteen, unpaddedSixteen)

        paddedSeventeen = addPKCS7Padding(seventeen, AES_BLOCK_SIZE)
        unpaddedSeventeen = stripPKCS7Padding(paddedSeventeen, AES_BLOCK_SIZE)
        self.assertEqual(seventeen, unpaddedSeventeen)


if __name__ == '__main__':
    unittest.main()

