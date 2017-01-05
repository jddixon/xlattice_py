#!/usr/bin/env python3
# dev/py/xlattice_py/test_re_struc.py

""" Test restructing of content-keyed store. """

import hashlib
import os
import unittest
#from binascii import hexlify

from rnglib import SimpleRNG
from xlattice import QQQ, check_using_sha
from xlattice.u import UDir  # ,SHA1_HEX_NONE, SHA2_HEX_NONE, SHA3_HEX_NONE


class TestReStruc(unittest.TestCase):
    """ Test restructing of content-keyed store. """

    def setUp(self):
        self.rng = SimpleRNG()

    def make_values(self, using_sha=False, m__=1, n__=1, l__=1):
        """
        Create at least m and then up to n more values of random length
        up to l (letter L) and compute their SHAx hashes.
        return list of values and a list of their hashes
        """

        check_using_sha(using_sha)

        # DEBUG
        #print("make_values: m__ = %d, n__ = %d, l__ = %d)" % (m__, n__, l__))
        # END
        if m__ <= 0:
            m__ = 1
        if n__ <= 0:
            n__ = 1
        if l__ <= 0:
            l__ = 1

        nnn = m__ + self.rng.next_int16(n__)       # random count of values

        values = []
        hex_hashes = []

        # DEBUG
        #print("VALUES AND HASHES")
        # END
        for _ in range(nnn):
            count = 1 + self.rng.next_int16(l__)   # so that count >= 1
            v__ = self.rng.some_bytes(count)       # that many random bytes
            values.append(v__)
            # pylint: disable=redefined-variable-type
            if using_sha == QQQ.USING_SHA1:
                sha = hashlib.sha1()
            elif using_sha == QQQ.USING_SHA2:
                sha = hashlib.sha256()
            elif using_sha == QQQ.USING_SHA3:
                # pylint: disable=no-member
                sha = hashlib.sha3_256()
            sha.update(v__)
            h__ = sha.hexdigest()
            # DEBUG
            #print("  %02d %s %s" % (_, hexlify(v).decode('utf8'),h__))
            # END
            hex_hashes.append(h__)

        return (values, hex_hashes)

    def do_test_re_struc(self, old_struc, new_struc, using_sha):
        """
        Create a unique test directory u_dir.  We expect this to write
        a characteristic signature into u_dir.
        """
        u_path = os.path.join('tmp', self.rng.next_file_name(8))
        while os.path.exists(u_path):
            u_path = os.path.join('tmp', self.rng.next_file_name(8))

        # DEBUG
        # print("\ncreating %-12s, old_struc=%s, new_struc=%s, using_sha=%s" % (
        #     u_path,
        #     UDir.dir_strucToName(old_struc),
        #     UDir.dir_strucToName(new_struc),
        #     using_sha))
        # END
        u_dir = UDir(u_path, old_struc, using_sha)
        self.assertEqual(using_sha, u_dir.using_sha)
        self.assertEqual(old_struc, u_dir.dir_struc)

        # Verify that the signature datum (SHAx_HEX_NONE) is present
        # in the file system.  How this is stored depends upon old_struc;
        # what value is stored depends upon using_sha.
        old_sig = u_dir.dir_struc_sig(u_path, old_struc, using_sha)
        self.assertTrue(os.path.exists(old_sig))

        values, hex_hashes = self.make_values(using_sha, 32, 32, 128)
        count = len(values)
        for nnn in range(count):
            u_dir.put_data(values[nnn], hex_hashes[nnn])
        # DEBUG
        # print("HASHES:")
        # END
        for nnn in range(count):
            # DEBUG
            #print("  %02d: %s" % (n, hex_hashes[nnn]))
            # END
            self.assertTrue(u_dir.exists(hex_hashes[nnn]))

        # restructure the directory
        u_dir.re_struc(new_struc)

        new_sig = u_dir.dir_struc_sig(u_path, new_struc, using_sha)
        self.assertTrue(os.path.exists(new_sig))
        self.assertFalse(os.path.exists(old_sig))

        for nnn in range(count):
            self.assertTrue(u_dir.exists(hex_hashes[nnn]))

        # XXX STUB: veriy any useless directories have been removed
        #   for example: if going from u_dir.DIR256x256 to UDir.DIR_FLAT,
        #   directoris like 00 and 00/00 should have been removed

    def test_re_struc(self):
        """ Test all combinations of dir structure and hash type. """
        for old_struc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for new_struc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
                if old_struc != new_struc:
                    for using in [QQQ.USING_SHA1, QQQ.USING_SHA2, ]:
                        self.do_test_re_struc(old_struc, new_struc, using)

if __name__ == '__main__':
    unittest.main()
