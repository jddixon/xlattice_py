#!/usr/bin/env python3

# xlattice_py/testU.py

import hashlib
import sha3     # must follow hashlib

import os
import time
import unittest
from xlattice import Q
from xlattice.u import (UDir,
                        file_sha1hex, file_sha1bin,
                        file_sha2hex, file_sha2bin,
                        file_sha3hex, file_sha3bin)

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

    def mapTest(self):
        for name in UDir.DIR_STRUC_NAMES:
            x = nameToDirStruc(name)
            name2 = dirStrucToName(x)
            self.assertEqual(name, name2)

    def doDiscoveryTest(self, dirStruc, usingSHA):

        uPath = os.path.join('tmp', self.rng.nextFileName(16))
        while os.path.exists(uPath):
            uPath = os.path.join('tmp', self.rng.nextFileName(16))

        uDir = UDir(uPath, dirStruc, usingSHA)
        self.assertEqual(uDir.uPath, uPath)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA, usingSHA)

        u2 = UDir.discover(uPath)
        self.assertEqual(u2.uPath, uPath)
        self.assertEqual(u2.dirStruc, dirStruc)
        # DEBUG
        if u2.usingSHA != usingSHA:
            print("doDiscoveryTest:")
            print("  dirStruc: %s" % UDir.DIR_STRUC_NAMES[dirStruc])
            print("  usingSHA: %s" % usingSHA)
        # END
        self.assertEqual(u2.usingSHA, usingSHA)

    def testDiscovery(self):
        for dirStruc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3]:
                self.doDiscoveryTest(dirStruc, using)

    # ---------------------------------------------------------------

    def doTestCopyAndPut(self, dirStruc, usingSHA):

        uDir = UDir(U_PATH, dirStruc, usingSHA)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA, usingSHA)

        for k in range(1024):
            # create a random file                            maxLen    minLen
            (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
            if usingSHA == Q.USING_SHA1:
                dKey = file_sha1hex(dPath)
            elif usingSHA == Q.USING_SHA2:
                dKey = file_sha2hex(dPath)
            elif usingSHA == Q.USING_SHA3:
                dKey = file_sha3hex(dPath)

            # copy this file into U
            (uLen, uKey) = uDir.copyAndPut(dPath, dKey)
            self.assertEqual(dLen, uLen)
            self.assertEqual(dKey, uKey)

            # verify that original and copy both exist
            self.assertTrue(os.path.exists(dPath))
            uPath = uDir.getPathForKey(uKey)
            self.assertTrue(os.path.exists(uPath))

            if usingSHA == Q.USING_SHA1:
                uKeyHex = file_sha1hex(uPath)
            elif usingSHA == Q.USING_SHA2:
                uKeyHex = file_sha2hex(uPath)
            elif usingSHA == Q.USING_SHA3:
                uKeyHex = file_sha3hex(uPath)
            self.assertEqual(uKeyHex, dKey)

    def testCopyAndPut(self):
        for dirStruc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3, ]:
                self.doTestCopyAndPut(dirStruc, using)

    # ---------------------------------------------------------------

    def doTestExists(self, dirStruc, usingSHA):
        """we are testing whether = uDir.exists(uPath, key) """

        uDir = UDir(U_PATH, dirStruc, usingSHA)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA, usingSHA)

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        if usingSHA == Q.USING_SHA1:
            dKey = file_sha1hex(dPath)
        elif usingSHA == Q.USING_SHA2:
            dKey = file_sha2hex(dPath)
        elif usingSHA == Q.USING_SHA3:
            dKey = file_sha3hex(dPath)
        (uLen, uKey) = uDir.copyAndPut(dPath, dKey)
        uPath = uDir.getPathForKey(uKey)
        self.assertTrue(os.path.exists(uPath))
        self.assertTrue(uDir.exists(uKey))
        os.unlink(uPath)
        self.assertFalse(os.path.exists(uPath))
        self.assertFalse(uDir.exists(uKey))

    def testExists(self):
        for dirStruc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3]:
                self.doTestExists(dirStruc, using)

    # ---------------------------------------------------------------

    def doTestFileLen(self, dirStruc, usingSHA):
        """we are testing len = uDir.fileLen(uPath, key) """

        uDir = UDir(U_PATH, dirStruc, usingSHA)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA, usingSHA)

        uDir = UDir(U_PATH, dirStruc, usingSHA)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA, usingSHA)

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        if usingSHA == Q.USING_SHA1:
            dKey = file_sha1hex(dPath)
        elif usingSHA == Q.USING_SHA2:
            dKey = file_sha2hex(dPath)
        elif usingSHA == Q.USING_SHA3:
            dKey = file_sha3hex(dPath)
        (uLen, uKey) = uDir.copyAndPut(dPath, dKey)
        uPath = uDir.getPathForKey(uKey)
        self.assertEqual(dLen, uLen)
        self.assertEqual(dLen, uDir.fileLen(uKey))

    def testFileLen(self):
        for dirStruc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3, ]:
                self.doTestFileLen(dirStruc, using)

    # ---------------------------------------------------------------

    def doTestFileSHA(self, dirStruc, usingSHA):
        """ we are testing shaXKey = file_shaXHex(path) """

        uDir = UDir(U_PATH, dirStruc, usingSHA)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA, usingSHA)

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        with open(dPath, 'rb') as f:
            data = f.read()
        if usingSHA == Q.USING_SHA1:
            digest = hashlib.sha1()
        elif usingSHA == Q.USING_SHA2:
            digest = hashlib.sha256()
        elif usingSHA == Q.USING_SHA3:
            digest = hashlib.sha3_256()
        digest.update(data)
        dKey = digest.hexdigest()
        if usingSHA == Q.USING_SHA1:
            fsha = file_sha1hex(dPath)
        elif usingSHA == Q.USING_SHA2:
            fsha = file_sha2hex(dPath)
        elif usingSHA == Q.USING_SHA3:
            fsha = file_sha3hex(dPath)
        self.assertEqual(dKey, fsha)

    def testFileSHA(self):
        for dirStruc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3, ]:
                self.doTestFileSHA(dirStruc, using)

    # ---------------------------------------------------------------
    def doTestGetPathForKey(self, dirStruc, usingSHA):
        """ we are testing path = getPathForKey(uPath, key) """

        uDir = UDir(U_PATH, dirStruc, usingSHA)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA, usingSHA)

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        if usingSHA == Q.USING_SHA1:
            dKey = file_sha1hex(dPath)
        elif usingSHA == Q.USING_SHA2:
            dKey = file_sha2hex(dPath)
        elif usingSHA == Q.USING_SHA3:
            dKey = file_sha3hex(dPath)
        (uLen, uKey) = uDir.copyAndPut(dPath, dKey)
        self.assertEqual(uKey, dKey)
        uPath = uDir.getPathForKey(uKey)

        # XXX implementation-dependent tests
        #
        if dirStruc == uDir.DIR_FLAT:
            expectedPath = os.path.join(U_PATH, uKey)
        elif dirStruc == uDir.DIR16x16:
            expectedPath = "%s/%s/%s/%s" % (U_PATH, uKey[0], uKey[1], uKey)
        elif dirStruc == uDir.DIR256x256:
            expectedPath = "%s/%s/%s/%s" % (U_PATH, uKey[0:2], uKey[2:4], uKey)
        else:
            self.fail("INTERNAL ERROR: unexpected dirStruc %d" % dirStruc)

        # DEBUG
        if expectedPath != uPath:
            if dirStruc == uDir.DIR_FLAT:
                print("uDir.DIR_FLAT")
            if dirStruc == uDir.DIR16x16:
                print("uDir.DIR16x16")
            if dirStruc == uDir.DIR256x256:
                print("uDir.DIR256x256")
            print("uPath:       %s" % uPath)
            print("expected:    %s" % expectedPath)
        # END

        self.assertEqual(expectedPath, uPath)

    def testGetPathForKey(self):
        for dirStruc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3, ]:
                self.doTestGetPathForKey(dirStruc, using)

    # ---------------------------------------------------------------

    def doTestPut(self, dirStruc, usingSHA):
        """we are testing (len,hash)  = put(inFile, uPath, key) """

        uDir = UDir(U_PATH, dirStruc, usingSHA)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA, usingSHA)

        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        if usingSHA == Q.USING_SHA1:
            dKey = file_sha1hex(dPath)
        elif usingSHA == Q.USING_SHA2:
            dKey = file_sha2hex(dPath)
        elif usingSHA == Q.USING_SHA3:
            dKey = file_sha3hex(dPath)
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
        for dirStruc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3, ]:
                self.doTestPut(dirStruc, using)

    # ---------------------------------------------------------------

    def doTestPutData(self, dirStruc, usingSHA):
        """
        We are testing (len,hash)  = putData(data, uPath, key)
        """

        uDir = UDir(U_PATH, dirStruc, usingSHA)
        self.assertEqual(uDir.uPath, U_PATH)
        self.assertEqual(uDir.dirStruc, dirStruc)
        self.assertEqual(uDir.usingSHA, usingSHA)

        # this is just lazy coding ;-)
        (dLen, dPath) = self.rng.nextDataFile(DATA_PATH, 16 * 1024, 1)
        if usingSHA == Q.USING_SHA1:
            dKey = file_sha1hex(dPath)
        elif usingSHA == Q.USING_SHA2:
            dKey = file_sha2hex(dPath)
        elif usingSHA == Q.USING_SHA3:
            dKey = file_sha3hex(dPath)
        with open(dPath, 'rb') as f:
            data = f.read()

        (uLen, uKey) = uDir.putData(data, dKey)
        self.assertEqual(dKey, uKey)
        self.assertTrue(uDir.exists(dKey))
        uPath = uDir.getPathForKey(uKey)             # GEEP

    def testPutData(self):
        for dirStruc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3, ]:
                self.doTestPutData(dirStruc, using)

if __name__ == '__main__':
    unittest.main()
