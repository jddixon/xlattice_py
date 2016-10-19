#!/usr/bin/env python3
# xlattice_py/testU.py

""" Test U and UDir functionality. """

import hashlib
import os
import time
import unittest

from xlattice import Q
from xlattice.u import (UDir, file_sha1hex, file_sha2hex, file_sha3hex)

from rnglib import SimpleRNG

DATA_PATH = 'myData'   # contains files of random data
U_PATH = 'myU1'        # those same files stored by content hash
U_TMP_PATH = 'myU1/tmp'


class TestU(unittest.TestCase):
    """ Test U and UDir functionality. """

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

    # XXX Never invoked; needs UDir parameter
#   def map_test(self):
#       """ Confirm that our map is working. """
#       for name in UDir.DIR_STRUC_NAMES:
#           xxx = name_to_dir_struc(name)
#           name2 = dir_struc_to_name(xxx)
#           self.assertEqual(name, name2)

    def do_discovery_test(self, dir_struc, using_sha):
        """ Verify that discovery of directory structure works. """

        u_path = os.path.join('tmp', self.rng.next_file_name(16))
        while os.path.exists(u_path):
            u_path = os.path.join('tmp', self.rng.next_file_name(16))

        u_dir = UDir(u_path, dir_struc, using_sha)
        self.assertEqual(u_dir.u_path, u_path)
        self.assertEqual(u_dir.dir_struc, dir_struc)
        self.assertEqual(u_dir.using_sha, using_sha)

        u2_ = UDir.discover(u_path)
        self.assertEqual(u2_.u_path, u_path)
        self.assertEqual(u2_.dir_struc, dir_struc)
        # DEBUG
        if u2_.using_sha != using_sha:
            print("do_discovery_test:")
            print("  dir_struc: %s" % UDir.DIR_STRUC_NAMES[dir_struc])
            print("  using_sha: %s" % using_sha)
        # END
        self.assertEqual(u2_.using_sha, using_sha)

    def test_discovery(self):
        """ Verify that discovery of directory structure works. """

        for dir_struc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3]:
                self.do_discovery_test(dir_struc, using)

    # ---------------------------------------------------------------

    def do_test_copy_and_put(self, dir_struc, using_sha):
        """ Check copying a directory structure into a content-keyed store."""

        u_dir = UDir(U_PATH, dir_struc, using_sha)
        self.assertEqual(u_dir.u_path, U_PATH)
        self.assertEqual(u_dir.dir_struc, dir_struc)
        self.assertEqual(u_dir.using_sha, using_sha)

        for _ in range(1024):
            # create a random file                            maxLen    minLen
            (d_len, d_path) = self.rng.next_data_file(DATA_PATH, 16 * 1024, 1)
            if using_sha == Q.USING_SHA1:
                d_key = file_sha1hex(d_path)
            elif using_sha == Q.USING_SHA2:
                d_key = file_sha2hex(d_path)
            elif using_sha == Q.USING_SHA3:
                d_key = file_sha3hex(d_path)

            # copy this file into U
            (u_len, u_key) = u_dir.copy_and_put(d_path, d_key)
            self.assertEqual(d_len, u_len)
            self.assertEqual(d_key, u_key)

            # verify that original and copy both exist
            self.assertTrue(os.path.exists(d_path))
            u_path = u_dir.get_path_for_key(u_key)
            self.assertTrue(os.path.exists(u_path))

            if using_sha == Q.USING_SHA1:
                u_key_kex = file_sha1hex(u_path)
            elif using_sha == Q.USING_SHA2:
                u_key_kex = file_sha2hex(u_path)
            elif using_sha == Q.USING_SHA3:
                u_key_kex = file_sha3hex(u_path)
            self.assertEqual(u_key_kex, d_key)

    def test_copy_and_put(self):
        """ Check copying a directory structure into a content-keyed store."""
        for dir_struc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3, ]:
                self.do_test_copy_and_put(dir_struc, using)

    # ---------------------------------------------------------------

    def do_test_exists(self, dir_struc, using_sha):
        """we are testing whether = u_dir.exists(u_path, key) """

        u_dir = UDir(U_PATH, dir_struc, using_sha)
        self.assertEqual(u_dir.u_path, U_PATH)
        self.assertEqual(u_dir.dir_struc, dir_struc)
        self.assertEqual(u_dir.using_sha, using_sha)

        (d_len, d_path) = self.rng.next_data_file(DATA_PATH, 16 * 1024, 1)
        if using_sha == Q.USING_SHA1:
            d_key = file_sha1hex(d_path)
        elif using_sha == Q.USING_SHA2:
            d_key = file_sha2hex(d_path)
        elif using_sha == Q.USING_SHA3:
            d_key = file_sha3hex(d_path)
        (u_len, u_key) = u_dir.copy_and_put(d_path, d_key)
        u_path = u_dir.get_path_for_key(u_key)
        self.assertTrue(os.path.exists(u_path))
        self.assertTrue(u_dir.exists(u_key))
        os.unlink(u_path)
        self.assertFalse(os.path.exists(u_path))
        self.assertFalse(u_dir.exists(u_key))

    def test_exists(self):
        """ Run existence tests over all combinations. """
        for dir_struc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3]:
                self.do_test_exists(dir_struc, using)

    # ---------------------------------------------------------------

    def do_test_file_len(self, dir_struc, using_sha):
        """we are testing len = u_dir.fileLen(u_path, key) """

        u_dir = UDir(U_PATH, dir_struc, using_sha)
        self.assertEqual(u_dir.u_path, U_PATH)
        self.assertEqual(u_dir.dir_struc, dir_struc)
        self.assertEqual(u_dir.using_sha, using_sha)

        u_dir = UDir(U_PATH, dir_struc, using_sha)
        self.assertEqual(u_dir.u_path, U_PATH)
        self.assertEqual(u_dir.dir_struc, dir_struc)
        self.assertEqual(u_dir.using_sha, using_sha)

        (d_len, d_path) = self.rng.next_data_file(DATA_PATH, 16 * 1024, 1)
        if using_sha == Q.USING_SHA1:
            d_key = file_sha1hex(d_path)
        elif using_sha == Q.USING_SHA2:
            d_key = file_sha2hex(d_path)
        elif using_sha == Q.USING_SHA3:
            d_key = file_sha3hex(d_path)
        (u_len, u_key) = u_dir.copy_and_put(d_path, d_key)
        u_path = u_dir.get_path_for_key(u_key)
        self.assertEqual(d_len, u_len)
        self.assertEqual(d_len, u_dir.file_len(u_key))

    def test_file_len(self):
        """ Test file_len() for all structures and hash types. """
        for dir_struc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3, ]:
                self.do_test_file_len(dir_struc, using)

    # ---------------------------------------------------------------

    def do_test_file_sha(self, dir_struc, using_sha):
        """ we are testing shaXKey = file_shaXHex(path) """

        u_dir = UDir(U_PATH, dir_struc, using_sha)
        self.assertEqual(u_dir.u_path, U_PATH)
        self.assertEqual(u_dir.dir_struc, dir_struc)
        self.assertEqual(u_dir.using_sha, using_sha)

        (d_len, d_path) = self.rng.next_data_file(DATA_PATH, 16 * 1024, 1)
        with open(d_path, 'rb') as file:
            data = file.read()
        # pylint: disable=redefined-variable-type
        if using_sha == Q.USING_SHA1:
            digest = hashlib.sha1()
        elif using_sha == Q.USING_SHA2:
            digest = hashlib.sha256()
        elif using_sha == Q.USING_SHA3:
            digest = hashlib.sha3_256()
        digest.update(data)
        d_key = digest.hexdigest()
        if using_sha == Q.USING_SHA1:
            fsha = file_sha1hex(d_path)
        elif using_sha == Q.USING_SHA2:
            fsha = file_sha2hex(d_path)
        elif using_sha == Q.USING_SHA3:
            fsha = file_sha3hex(d_path)
        self.assertEqual(d_key, fsha)

    def test_file_sha(self):
        """ Verify content keys match file names for combinations. """
        for dir_struc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3, ]:
                self.do_test_file_sha(dir_struc, using)

    # ---------------------------------------------------------------
    def do_test_get_path_for_key(self, dir_struc, using_sha):
        """ we are testing path = get_path_for_key(u_path, key) """

        u_dir = UDir(U_PATH, dir_struc, using_sha)
        self.assertEqual(u_dir.u_path, U_PATH)
        self.assertEqual(u_dir.dir_struc, dir_struc)
        self.assertEqual(u_dir.using_sha, using_sha)

        (d_len, d_path) = self.rng.next_data_file(DATA_PATH, 16 * 1024, 1)
        if using_sha == Q.USING_SHA1:
            d_key = file_sha1hex(d_path)
        elif using_sha == Q.USING_SHA2:
            d_key = file_sha2hex(d_path)
        elif using_sha == Q.USING_SHA3:
            d_key = file_sha3hex(d_path)
        (u_len, u_key) = u_dir.copy_and_put(d_path, d_key)
        self.assertEqual(u_key, d_key)
        u_path = u_dir.get_path_for_key(u_key)

        # XXX implementation-dependent tests
        #
        if dir_struc == u_dir.DIR_FLAT:
            expected_path = os.path.join(U_PATH, u_key)
        elif dir_struc == u_dir.DIR16x16:
            expected_path = "%s/%s/%s/%s" % (U_PATH, u_key[0], u_key[1], u_key)
        elif dir_struc == u_dir.DIR256x256:
            expected_path = "%s/%s/%s/%s" % (U_PATH,
                                             u_key[0:2], u_key[2:4], u_key)
        else:
            self.fail("INTERNAL ERROR: unexpected dir_struc %d" % dir_struc)

        # DEBUG
        if expected_path != u_path:
            if dir_struc == u_dir.DIR_FLAT:
                print("u_dir.DIR_FLAT")
            if dir_struc == u_dir.DIR16x16:
                print("u_dir.DIR16x16")
            if dir_struc == u_dir.DIR256x256:
                print("u_dir.DIR256x256")
            print("u_path:       %s" % u_path)
            print("expected:    %s" % expected_path)
        # END

        self.assertEqual(expected_path, u_path)

    def test_get_path_for_key(self):
        """ Verify path correct for content for all combinations. """

        for dir_struc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3, ]:
                self.do_test_get_path_for_key(dir_struc, using)

    # ---------------------------------------------------------------

    def do_test_put(self, dir_struc, using_sha):
        """we are testing (len,hash)  = put(inFile, u_path, key) """

        u_dir = UDir(U_PATH, dir_struc, using_sha)
        self.assertEqual(u_dir.u_path, U_PATH)
        self.assertEqual(u_dir.dir_struc, dir_struc)
        self.assertEqual(u_dir.using_sha, using_sha)

        (d_len, d_path) = self.rng.next_data_file(DATA_PATH, 16 * 1024, 1)
        if using_sha == Q.USING_SHA1:
            d_key = file_sha1hex(d_path)
        elif using_sha == Q.USING_SHA2:
            d_key = file_sha2hex(d_path)
        elif using_sha == Q.USING_SHA3:
            d_key = file_sha3hex(d_path)
        with open(d_path, 'rb') as file:
            data = file.read()
        dupe_path = os.path.join(DATA_PATH, d_key)
        with open(dupe_path, 'wb') as file:
            file.write(data)

        (u_len, u_key) = u_dir.put(d_path, d_key)
        u_path = u_dir.get_path_for_key(u_key)

        # inFile is renamed
        self.assertFalse(os.path.exists(d_path))
        self.assertTrue(u_dir.exists(u_key))

        (dupe_len, dupe_key) = u_dir.put(dupe_path, d_key)
        # dupe file is deleted'
        self.assertEqual(u_key, dupe_key)
        self.assertFalse(os.path.exists(dupe_path))
        self.assertTrue(u_dir.exists(u_key))

    def test_put(self):
        """ Verify len,hash correct on file puts for all combinations. """

        for dir_struc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3, ]:
                self.do_test_put(dir_struc, using)

    # ---------------------------------------------------------------

    def do_test_put_data(self, dir_struc, using_sha):
        """
        We are testing (len,hash)  = put_data(data, u_path, key)
        """

        u_dir = UDir(U_PATH, dir_struc, using_sha)
        self.assertEqual(u_dir.u_path, U_PATH)
        self.assertEqual(u_dir.dir_struc, dir_struc)
        self.assertEqual(u_dir.using_sha, using_sha)

        # this is just lazy coding ;-)
        (d_len, d_path) = self.rng.next_data_file(DATA_PATH, 16 * 1024, 1)
        if using_sha == Q.USING_SHA1:
            d_key = file_sha1hex(d_path)
        elif using_sha == Q.USING_SHA2:
            d_key = file_sha2hex(d_path)
        elif using_sha == Q.USING_SHA3:
            d_key = file_sha3hex(d_path)
        with open(d_path, 'rb') as file:
            data = file.read()

        (u_len, u_key) = u_dir.put_data(data, d_key)
        self.assertEqual(d_key, u_key)
        self.assertTrue(u_dir.exists(d_key))
        u_path = u_dir.get_path_for_key(u_key)             # GEEP

    def test_put_data(self):
        """ Verify len,hash correct on data puts for all combinations. """

        for dir_struc in [UDir.DIR_FLAT, UDir.DIR16x16, UDir.DIR256x256]:
            for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3, ]:
                self.do_test_put_data(dir_struc, using)

if __name__ == '__main__':
    unittest.main()
