#!/usr/bin/env python3

# xlattice_py/testHelloAndReply.py

import os
import time
import unittest
# from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import rnglib

import xlattice.hello_and_reply as hr
from xlattice.util import DecimalVersion, parse_decimal_version
from xlattice import SHA1_BIN_LEN

KEY_BITS = 2048
KEY_BYTES = KEY_BITS / 8
MAX_MSG = KEY_BYTES - 1 - 2 * SHA1_BIN_LEN  # one more than max value

TEST_DIR = 'tmp'


class TestRSA_OAEP(unittest.TestCase):

    def setUp(self):
        now = time.time()
        self.rng = rnglib.SimpleRNG(now)
        if not os.path.exists(TEST_DIR):
            os.makedirs(TEST_DIR)

    def tearDown(self):
        pass

    def test_encrypt_decrypt(self):

        # set up private RSA key, get its public part
        # generate a 2K bit private key
        ck_priv = RSA.generate(KEY_BITS)
        # self.assertEqual(ckPriv.size(), KEY_BITS) # fails, may be a little
        # less
        ck_ = ck_priv.publickey()
        self.assertEqual(ck_.has_private(), False)

        # prepare DecimalVersion object, get its value, an int
        www = self.rng.nextInt16(256)
        xxx = self.rng.nextInt16(256)
        yyy = self.rng.nextInt16(256)
        zzz = self.rng.nextInt16(256)
        version_obj = DecimalVersion(www, xxx, yyy, zzz)
        version = version_obj.value            # a property
        serial_version = '%d.%d.%d.%d' % (www, xxx, yyy, zzz)
        version_from_s = parse_decimal_version(serial_version)
        self.assertEqual(version, version_from_s.value)

        # CLIENT ENCRYPTS HELLO -------------------------------------

        encrypted_hello, iv1, key1, salt1 = hr.client_encrypt_hello(
            version, ck_)
        self.assertEqual(len(encrypted_hello), KEY_BITS / 8)
        self.assertEqual(len(iv1), hr.AES_BLOCK_SIZE)
        self.assertEqual(len(key1), 2 * hr.AES_BLOCK_SIZE)
        self.assertEqual(len(salt1), 8)

        # SERVER DECRYPTS HELLO -------------------------------------
        iv1s, key1s, salt1s, version_s = hr.server_decrypt_hello(
            encrypted_hello, ck_priv)

        # in real use, the server could require a different version
        self.assertEqual(version_s, version)
        self.assertEqual(iv1, iv1s)
        self.assertEqual(key1, key1s)
        self.assertEqual(salt1, salt1s)

        # SERVER PREPARES AND ENCRYPTS REPLY ------------------------
        version2s = self.rng.nextInt32()
        iv2s, key2s, salt2s, encrypted_reply = hr.server_encrypt_hello_reply(
            iv1, key1, salt1, version2s)

        # CLIENT DECRYPTS REPLY -------------------------------------
        iv2, key2, salt2, salt1x, version2 = hr.client_decrypt_hello_reply(
            encrypted_reply, iv1, key1)

        self.assertEqual(iv2, iv2s)
        self.assertEqual(key2, key2s)
        self.assertEqual(salt2, salt2s)
        self.assertEqual(salt1x, salt1)
        _ = version2                        # unused

if __name__ == '__main__':
    unittest.main()