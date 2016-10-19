#!/usr/bin/env python3

import binascii
import sys
import unittest
import hashlib
if sys.version_info < (3, 6):
    import sha3                     # pysha3

from xlattice import SHA3_HEX_NONE, SHA3_BIN_NONE


class TestSHA3_256(unittest.TestCase):

    SHA3_NAME = "sha3_256"
    DIGEST_SIZE = 32    # bytes
    BLOCK_SIZE = 136   # bytes (so 1088 bits, not 1600)
    HEX_VECTORS = [
        ('', 'a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a'),

        # GET MORE FROM NIST DOCS

    ]
    U2H_VECTORS = [
        ('abc',
            '3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532'),
        # GET MORE FROM NIST DOCS

    ]

    def testConstructor(self):
        """ verify that behavior of pysha3 is as expected """

        sha = hashlib.sha3_256()

        # verify it has the right properties ...
        self.assertEqual(sha.name, self.SHA3_NAME)
        self.assertEqual(sha.digest_size, self.DIGEST_SIZE)
        self.assertEqual(len(sha.digest()), self.DIGEST_SIZE)
        self.assertEqual(len(sha.hexdigest()), self.DIGEST_SIZE * 2)
        self.assertEqual(sha.block_size, self.BLOCK_SIZE)

        # we shouldn't be able to assign to properties
        self.assertRaises(AttributeError, setattr, sha, "digest", 42)
        self.assertRaises(AttributeError, setattr, sha, "name", "foo")

        # byte strings are acceptable parameters
        hashlib.sha3_256(b"foo")
        hashlib.sha3_256(string=b"foo")

        # None is not an acceptable parameter to the constructor
        self.assertRaises(TypeError, hashlib.sha3_256, None)
        # neitheris unicode
        self.assertRaises(TypeError, hashlib.sha3_256, "abcdef")

        # same constraints on parameters to update()
        self.assertRaises(TypeError, sha.update, None)
        self.assertRaises(TypeError, sha.update, "abcdef")

    def testConstants(self):
        sha = hashlib.sha3_256()
        sha.update(b'')
        self.assertEqual(sha.digest(), SHA3_BIN_NONE)
        self.assertEqual(sha.hexdigest(), SHA3_HEX_NONE)

    def testHexVectors(self):
        for hexIn, expectedHexOut in self.HEX_VECTORS:
            self.doTestHexInOut(hexIn, expectedHexOut)

    def testUnicodeToHexVectors(self):
        for uniIn, expectedHexOut in self.U2H_VECTORS:
            # requires py3.5:
            # hexIn = uniIn.encode('utf-8').hex()
            hexIn = (binascii.hexlify(uniIn.encode('utf-8'))).decode('ascii')
            self.doTestHexInOut(hexIn, expectedHexOut)

    def doTestHexInOut(self, hexIn, expectedHexOut):
        expectedHexOut = expectedHexOut.lower()
        binIn = bytes.fromhex(hexIn)
        expectedBinOut = bytes.fromhex(expectedHexOut)
        self.assertEqual(len(expectedBinOut), self.DIGEST_SIZE)

        # shortcut passes bytes to constructor
        sha = hashlib.sha3_256(binIn)
        self.assertEqual(sha.hexdigest(), expectedHexOut)
        self.assertEqual(sha.digest(), expectedBinOut)

        # longer version has an explicit update() call
        sha = hashlib.sha3_256()
        sha.update(binIn)
        self.assertEqual(sha.hexdigest(), expectedHexOut)
        self.assertEqual(sha.digest(), expectedBinOut)

        # we can also hash the binary value byte by byte
        sha = hashlib.sha3_256()
        for bVal in binIn:
            x = bytearray(1)
            x[0] = bVal
            sha.update(x)
        self.assertEqual(sha.hexdigest(), expectedHexOut)
        self.assertEqual(sha.digest(), expectedBinOut)


if __name__ == "__main__":
    unittest.main()
