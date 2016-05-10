#!/usr/bin/python3

# xlattice_py/testSHA2.py

import binascii
import os
import re
import time
import unittest
import hashlib
import sys
from xlattice import u
from rnglib import SimpleRNG

DATA_PATH = 'myData'
U_PATH = 'myU2'
U_TMP_PATH = 'myU2/tmp'

#######################################################
# OBSOLESCENT: THIS FILE IS REPLACED BY testU256SHA2.py
#######################################################


class TestSHA2 (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())
        if not os.path.exists(DATA_PATH):
            os.mkdir(DATA_PATH)
        if not os.path.exists(U_PATH):
            os.mkdir(U_PATH)
        if not os.path.exists(U_TMP_PATH):
            os.mkdir(U_TMP_PATH)

    def tearDown(self):
        # probably should clear DATA_PATH and U_PATH directories
        pass

    # utility functions #############################################

    # actual unit tests #############################################
    def testCopyAndPut(self):
        """we are testing sha1Key = u.copyAndPut2(path, uPath, key) """

        # create a random file                          maxLen   minLen
        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        dKey = u.fileSHA2Hex(dPath)

        # invoke function
        (uLen, uKey) = u.copyAndPut2(dPath, U_PATH, dKey)
        self.assertEqual(dLen, uLen)
        self.assertEqual(dKey, uKey)

        # verify that original and copy both exist
        self.assertTrue(os.path.exists(dPath))
        uPath = u.getPathForKey(U_PATH, uKey)
        self.assertTrue(os.path.exists(uPath))

        dKeyBin = u.fileSHA2Bin(dPath)
        dKeyHex = binascii.b2a_hex(dKeyBin).decode('utf-8')
        self.assertEqual(dKeyHex, dKey)

    def testExists(self):
        """we are testing whether = u.exists(uPath, key) """

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        dKey = u.fileSHA2Hex(dPath)
        (uLen, uKey) = u.copyAndPut2(dPath, U_PATH, dKey)
        uPath = u.getPathForKey(U_PATH, uKey)
        self.assertTrue(os.path.exists(uPath))
        self.assertTrue(u.exists(U_PATH, uKey))
        os.unlink(uPath)
        self.assertFalse(os.path.exists(uPath))
        self.assertFalse(u.exists(U_PATH, uKey))

    def testFileLen(self):
        """we are testing len = u.fileLen(uPath, key) """

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        dKey = u.fileSHA2Hex(dPath)
        (uLen, uKey) = u.copyAndPut2(dPath, U_PATH, dKey)
        uPath = u.getPathForKey(U_PATH, uKey)
        self.assertEqual(dLen, uLen)
        self.assertEqual(dLen, u.fileLen(U_PATH, uKey))

    def testFileSHA2(self):
        """ we are testing sha1Key = fileSHA2Hex(path) """
        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        with open(dPath, 'rb') as f:
            data = f.read()
        digest = hashlib.sha256()
        digest.update(data)
        dKey = digest.hexdigest()
        fsha1 = u.fileSHA2Hex(dPath)
        self.assertEqual(dKey, fsha1)

    def testGetPathForKey(self):
        """ we are testing path = getPathForKey(uPath, key) """

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        dKey = u.fileSHA2Hex(dPath)
        (uLen, uKey) = u.copyAndPut2(dPath, U_PATH, dKey)
        uPath = u.getPathForKey(U_PATH, uKey)

        # XXX implementation-dependent test
        expectedPath = "%s/%s/%s/%s" % (U_PATH, uKey[0:2], uKey[2:4], uKey)
        self.assertEqual(expectedPath, uPath)

    def testPut(self):
        """we are testing (len,hash)  = put(inFile, uPath, key) """

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        dKey = u.fileSHA2Hex(dPath)
        with open(dPath, 'rb') as f:
            data = f.read()
        dupePath = os.path.join(DATA_PATH, dKey)
        with open(dupePath, 'wb') as f:
            f.write(data)

        (uLen, uKey) = u.put2(dPath, U_PATH, dKey)
        uPath = u.getPathForKey(U_PATH, uKey)

        # inFile is renamed
        self.assertFalse(os.path.exists(dPath))
        self.assertTrue(u.exists(U_PATH, uKey))

        (dupeLen, dupeKey) = u.put2(dupePath, U_PATH, dKey)
        # dupe file is deleted'
        self.assertEqual(uKey, dupeKey)
        self.assertFalse(os.path.exists(dupePath))
        self.assertTrue(u.exists(U_PATH, uKey))

    def testPutData(self):
        """ we are testing (len,hash)  = putData2(data, uPath, key) """

        # this is just lazy coding ;-)
        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        dKey = u.fileSHA2Hex(dPath)
        with open(dPath, 'rb') as f:
            data = f.read()

        (uLen, uKey) = u.putData2(data, U_PATH, dKey)
        self.assertEqual(dKey, uKey)
        self.assertTrue(u.exists(U_PATH, dKey))
        uPath = u.getPathForKey(U_PATH, uKey)


if __name__ == '__main__':
    unittest.main()
