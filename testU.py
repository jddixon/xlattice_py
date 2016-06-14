#!/usr/bin/env python3

# xlattice_py/testU.py

import hashlib
import os
import time
import unittest
from xlattice.u import (UDir, DIR_FLAT, DIR16x16, DIR256x256,
                        fileSHA1Hex, fileSHA1Bin,
                        fileSHA2Hex, fileSHA2Bin)

from rnglib import SimpleRNG

DATA_PATH = 'myData'      # contains files of random data
U_PATH = 'myU1'        # those same files stored by content hash
U_TMP_PATH = 'myU1/tmp'


class TestU (unittest.TestCase):

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

    # actual unit tests =============================================

    def doDiscoveryTest(self, dirStruc, usingSHA1):

        uPath = os.path.join('tmp', self.rng.nextFileName(16))
        while os.path.exists(uPath):
            uPath = os.path.join('tmp', self.rng.nextFileName(16))

        uDir = UDir(uPath, dirStruc, usingSHA1)
        self.assertEqual(uDir.uPath, uPath)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA1, usingSHA1)

        u2 = UDir.discover(uPath)
        self.assertEqual(u2.uPath, uPath)
        self.assertEqual(u2.dirStruc, dirStruc)
        self.assertEqual(u2.usingSHA1, usingSHA1)

    def testDiscovery(self):
        for dirStruc in [DIR_FLAT, DIR16x16, DIR256x256]:
            self.doDiscoveryTest(dirStruc, True)
            self.doDiscoveryTest(dirStruc, False)

    # ---------------------------------------------------------------

    def doTestCopyAndPut(self, dirStruc, usingSHA1):

        uDir = UDir(U_PATH, dirStruc, usingSHA1)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA1, usingSHA1)

        for k in range(1024):
            # create a random file                            maxLen    minLen
            (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
            if usingSHA1:
                dKey = fileSHA1Hex(dPath)
            else:
                dKey = fileSHA2Hex(dPath)

            # copy this file into U
            (uLen, uKey) = uDir.copyAndPut(dPath, dKey)
            self.assertEqual(dLen, uLen)
            self.assertEqual(dKey, uKey)

            # verify that original and copy both exist
            self.assertTrue(os.path.exists(dPath))
            uPath = uDir.getPathForKey(uKey)
            self.assertTrue(os.path.exists(uPath))

            if usingSHA1:
                uKeyHex = fileSHA1Hex(uPath)
            else:
                uKeyHex = fileSHA2Hex(uPath)
            self.assertEqual(uKeyHex, dKey)

    def testCopyAndPut(self):
        for dirStruc in [DIR_FLAT, DIR16x16, DIR256x256]:
            self.doTestCopyAndPut(dirStruc, True)
            self.doTestCopyAndPut(dirStruc, False)

    # ---------------------------------------------------------------

    def doTestExists(self, dirStruc, usingSHA1):
        """we are testing whether = uDir.exists(uPath, key) """

        uDir = UDir(U_PATH, dirStruc, usingSHA1)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA1, usingSHA1)

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        if usingSHA1:
            dKey = fileSHA1Hex(dPath)
        else:
            dKey = fileSHA2Hex(dPath)
        (uLen, uKey) = uDir.copyAndPut(dPath, dKey)
        uPath = uDir.getPathForKey(uKey)
        self.assertTrue(os.path.exists(uPath))
        self.assertTrue(uDir.exists(uKey))
        os.unlink(uPath)
        self.assertFalse(os.path.exists(uPath))
        self.assertFalse(uDir.exists(uKey))

    def testExists(self):
        for dirStruc in [DIR_FLAT, DIR16x16, DIR256x256]:
            self.doTestExists(dirStruc, True)
            self.doTestExists(dirStruc, False)

    # ---------------------------------------------------------------

    def doTestFileLen(self, dirStruc, usingSHA1):
        """we are testing len = uDir.fileLen(uPath, key) """

        uDir = UDir(U_PATH, dirStruc, usingSHA1)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA1, usingSHA1)

        uDir = UDir(U_PATH, dirStruc, usingSHA1)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA1, usingSHA1)

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        if usingSHA1:
            dKey = fileSHA1Hex(dPath)
        else:
            dKey = fileSHA2Hex(dPath)
        (uLen, uKey) = uDir.copyAndPut(dPath, dKey)
        uPath = uDir.getPathForKey(uKey)
        self.assertEqual(dLen, uLen)
        self.assertEqual(dLen, uDir.fileLen(uKey))

    def testFileLen(self):
        for dirStruc in [DIR_FLAT, DIR16x16, DIR256x256]:
            self.doTestFileLen(dirStruc, True)

    # ---------------------------------------------------------------

    def doTestFileSHA(self, dirStruc, usingSHA1):
        """ we are testing shaXKey = fileSHAXHex(path) """

        uDir = UDir(U_PATH, dirStruc, usingSHA1)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA1, usingSHA1)

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        with open(dPath, 'rb') as f:
            data = f.read()
        if usingSHA1:
            digest = hashlib.sha1()
        else:
            digest = hashlib.sha256()
        digest.update(data)
        dKey = digest.hexdigest()
        if usingSHA1:
            fsha = fileSHA1Hex(dPath)
        else:
            fsha = fileSHA1Hex(dPath)
        self.assertEqual(dKey, fsha)

    def testFileSHA(self):
        for dirStruc in [DIR_FLAT, DIR16x16, DIR256x256]:
            self.doTestFileSHA(dirStruc, True)

    # ---------------------------------------------------------------
    def doTestGetPathForKey(self, dirStruc, usingSHA1):
        """ we are testing path = getPathForKey(uPath, key) """

        uDir = UDir(U_PATH, dirStruc, usingSHA1)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA1, usingSHA1)

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        if usingSHA1:
            dKey = fileSHA1Hex(dPath)
        else:
            dKey = fileSHA2Hex(dPath)
        (uLen, uKey) = uDir.copyAndPut(dPath, dKey)
        self.assertEqual(uKey, dKey)
        uPath = uDir.getPathForKey(uKey)

        # XXX implementation-dependent tests
        #
        if dirStruc == DIR_FLAT:
            expectedPath = os.path.join(U_PATH, uKey)
        elif dirStruc == DIR16x16:
            expectedPath = "%s/%s/%s/%s" % (U_PATH, uKey[0], uKey[1], uKey)
        elif dirStruc == DIR256x256:
            expectedPath = "%s/%s/%s/%s" % (U_PATH, uKey[0:2], uKey[2:4], uKey)
        else:
            self.fail("INTERNAL ERROR: unexpected dirStruc 0x%x" % dirStruc)

        # DEBUG
        if expectedPath != uPath:
            if dirStruc == DIR_FLAT:
                print("DIR_FLAT")
            if dirStruc == DIR16x16:
                print("DIR16x16")
            if dirStruc == DIR256x256:
                print("DIR256x256")
            print("uPath:       %s" % uPath)
            print("expected:    %s" % expectedPath)
        # END

        self.assertEqual(expectedPath, uPath)

    def testGetPathForKey(self):
        for dirStruc in [DIR_FLAT, DIR16x16, DIR256x256]:
            self.doTestGetPathForKey(dirStruc, True)

    # ---------------------------------------------------------------

    def doTestPut(self, dirStruc, usingSHA1):
        """we are testing (len,hash)  = put(inFile, uPath, key) """

        uDir = UDir(U_PATH, dirStruc, usingSHA1)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA1, usingSHA1)

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        if usingSHA1:
            dKey = fileSHA1Hex(dPath)
        else:
            dKey = fileSHA2Hex(dPath)
        with open(dPath, 'rb') as f:
            data = f.read()
        dupePath = os.path.join(DATA_PATH, dKey)
        with open(dupePath, 'wb') as f:
            f.write(data)

        (uLen, uKey) = uDir.put(dPath, dKey)
        uPath = uDir.getPathForKey(uKey)

        # inFile is renamed
        self.assertFalse(os.path.exists(dPath))
        self.assertTrue(uDir.exists(uKey))

        (dupeLen, dupeKey) = uDir.put(dupePath, dKey)
        # dupe file is deleted'
        self.assertEqual(uKey, dupeKey)
        self.assertFalse(os.path.exists(dupePath))
        self.assertTrue(uDir.exists(uKey))

    def testPut(self):
        for dirStruc in [DIR_FLAT, DIR16x16, DIR256x256]:
            self.doTestPut(dirStruc, True)

    # ---------------------------------------------------------------

    def doTestPutData(self, dirStruc, usingSHA1):
        """
        We are testing (len,hash)  = putData(data, uPath, key)
        """

        uDir = UDir(U_PATH, dirStruc, usingSHA1)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA1, usingSHA1)

        # this is just lazy coding ;-)
        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        if usingSHA1:
            dKey = fileSHA1Hex(dPath)
        else:
            dKey = fileSHA2Hex(dPath)
        with open(dPath, 'rb') as f:
            data = f.read()

        (uLen, uKey) = uDir.putData(data, dKey)
        self.assertEqual(dKey, uKey)
        self.assertTrue(uDir.exists(dKey))
        uPath = uDir.getPathForKey(uKey)             # GEEP

    def testPutData(self):
        for dirStruc in [DIR_FLAT, DIR16x16, DIR256x256]:
            self.doTestPutData(dirStruc, True)

if __name__ == '__main__':
    unittest.main()