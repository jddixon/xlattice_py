#!/usr/bin/env python3

# dev/py/xlattice_py/testReStruc.py

import hashlib
import os
import sys
import unittest
from binascii import hexlify

from rnglib import SimpleRNG
from xlattice.stats import UStats
from xlattice.u import (SHA1_HEX_NONE, SHA2_HEX_NONE, UDir)


class TestReStruc (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG()

    def makeValues(self, usingSHA1=False, m=1, n=1, l=1):
        """
        Create at least m and then up to n more values of random length
        up to l (letter L) and compute their SHAx hashes.
        return list of values and a list of their hashes
        """
        # DEBUG
        #print("makeValues: m = %d, n = %d, l = %d)" % (m, n, l))
        # END
        if m <= 0:
            m = 1
        if n <= 0:
            n = 1
        if l <= 0:
            l = 1

        N = m + self.rng.nextInt16(n)       # random count of values

        values = []
        hexHashes = []

        # DEBUG
        #print("VALUES AND HASHES")
        # END
        for i in range(N):
            count = 1 + self.rng.nextInt16(l)   # so that count >= 1
            v = self.rng.someBytes(count)       # that many random bytes
            values.append(v)
            if usingSHA1:
                sha = hashlib.sha1()
            else:
                sha = hashlib.sha256()
            sha.update(v)
            h = sha.hexdigest()
            # DEBUG
            #print("  %02d %s %s" % (i, hexlify(v).decode('utf8'),h))
            # END
            hexHashes.append(h)

        return (values, hexHashes)

    def doTestReStruc(self, oldStruc, newStruc, usingSHA1):

        # Create a unique test directory uDir.  We expect this to write
        # a characteristic signature into uDir.
        uPath = os.path.join('tmp', self.rng.nextFileName(8))
        while os.path.exists(uPath):
            uPath = os.path.join('tmp', self.rng.nextFileName(8))
        # DEBUG
        # print("\ncreating %-12s, oldStruc=%s, newStruc=%s, usingSHA1=%s" % (
        #     uPath,
        #     UDir.dirStrucToName(oldStruc),
        #     UDir.dirStrucToName(newStruc),
        #     usingSHA1))
        # END
        uDir = UDir(uPath, oldStruc, usingSHA1)
        self.assertEqual(usingSHA1, uDir.usingSHA1)
        self.assertEqual(oldStruc, uDir.dirStruc)

        # Verify that the signature datum (SHAx_HEX_NONE) is present
        # in the file system.  How this is stored depends upon oldStruc;
        # what value is stored depends upon usingSHA1.
        oldSig = UDir.dirStrucSig(uPath, oldStruc, usingSHA1)
        self.assertTrue(os.path.exists(oldSig))

        values, hexHashes = self.makeValues(usingSHA1, 32, 32, 128)
        K = len(values)
        for n in range(K):
            uDir.putData(values[n], hexHashes[n])
        # DEBUG
        # print("HASHES:")
        # END
        for n in range(K):
            # DEBUG
            #print("  %02d: %s" % (n, hexHashes[n]))
            # END
            self.assertTrue(uDir.exists(hexHashes[n]))

        # restructure the directory
        uDir.reStruc(newStruc)

        newSig = UDir.dirStrucSig(uPath, newStruc, usingSHA1)
        self.assertTrue(os.path.exists(newSig))
        self.assertFalse(os.path.exists(oldSig))

        for n in range(K):
            self.assertTrue(uDir.exists(hexHashes[n]))

        # XXX STUB: veriy any useless directories have been removed
        #   for example: if going from uDir.DIR256x256 to UDir.DIR_FLAT,
        #   directoris like 00 and 00/00 should have been removed

    def testReStruc(self):
        for oldStruc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for newStruc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
                if oldStruc != newStruc:
                    self.doTestReStruc(oldStruc, newStruc, True)
                    self.doTestReStruc(oldStruc, newStruc, False)

if __name__ == '__main__':
    unittest.main()
