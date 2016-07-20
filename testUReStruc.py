#!/usr/bin/env python3

# dev/py/xlattice_py/testReStruc.py

import hashlib
import os
import sys
import unittest
from rnglib import SimpleRNG
from xlattice.stats import UStats
from xlattice.u import (DIR_FLAT, DIR16x16, DIR256x256, DIR_STRUC_MAX,
                        SHA1_HEX_NONE, SHA2_HEX_NONE, dirStrucSig,
                        UDir)


class TestReStruc (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG()

    def makeValues(self, usingSHA1=False, m=1, n=1, l=1):
        """
        Create at least m and then up to n more values of random length
        up to l (letter L) and compute their SHAx hashes.
        return list of values and a list of their hashes
        """
        if m <= 0:
            m = 1
        if n <= 0:
            n = 1
        if l <= 0:
            l = 1

        N = m + self.rng.nextInt16(n)       # random count of values

        values = []
        hexHashes = []

        for i in range(N):
            count = self.rng.nextInt16(l)   # so that count < l
            v = self.rng.someBytes(count)   # that many random bytes
            values.append(v)
            if usingSHA1:
                sha = hashlib.sha1()
            else:
                sha = hashlib.sha256()
            sha.update(v)
            hexHashes.append(sha.hexdigest())

        return (values, hexHashes)

    def doTestReStruc(self, dirStruc, usingSHA1):
        # Create a unique test directory uDir.  We expect this to write
        # a characteristic signature into uDir.
        uPath = os.path.join('tmp', self.rng.nextFileName(8))
        while os.path.exists(uPath):
            uPath = os.path.join('tmp', self.rng.nextFileName(8))
        uDir = UDir(uPath, dirStruc, usingSHA1)
        self.assertEqual(usingSHA1, uDir.usingSHA1)
        self.assertEqual(dirStruc, uDir.dirStruc)

        # Verify that the signature datum (SHAx_HEX_NONE) is present
        # in the file system.  How this is stored depends upon dirStruc;
        # what value is stored depends upon usingSHA1.
        sig = dirStrucSig(uPath, dirStruc, usingSHA1)
        self.assertTrue(os.path.exists(sig))

        values, hexHashes = self.makeValues(32, 32, 128)
        k = len(values)
        for n in range(k):
            uDir.putData(values[n], hexHashes[n])
        for n in range(k):
            # DEBUG
            print("%02d: %s" % (n, hexHashes[n]))
            # END
            self.assertTrue(uDir.exists(hexHashes[n]))

        # select 'next' dirStruc (treat dirStruc as a ring)
        dirStruc2 = (dirStruc + 1) % DIR_STRUC_MAX

        # XXX STUB: restructure the directory

        # XXX STUB: calculate sig2
        # XXX STUB: verify sig2 is present in uDir
        # XXX STUB: verify sig  is NOT present in uDir

        for n in range(k):
            self.assertTrue(uDir.exists(hexHashes[n]))

        # XXX STUB: veriy any useless directories have been removed
        #   for example: if going from DIR256x256 to DIR_FLAT,
        #   directoris like 00 and 00/00 should have been removed

    def testReStruc(self):
        for dirStruc in [DIR_FLAT, DIR16x16, DIR256x256]:
            for usingSHA1 in [True, False]:
                self.doTestReStruc(dirStruc, usingSHA1)

if __name__ == '__main__':
    unittest.main()
