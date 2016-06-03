#!/usr/bin/env python3

# xlattice_py/testHelloAndReply.py

import os
import sys
import time
import unittest
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import rnglib

import xlattice.helloAndReply as hr
from xlattice.util import DecimalVersion, parseDecimalVersion
from xlattice import SHA1_BIN_LEN

KEY_BITS = 2048
KEY_BYTES = KEY_BITS / 8
MAX_MSG = KEY_BYTES - 1 - 2 * SHA1_BIN_LEN  # one more than max value

TEST_DIR = 'tmp'


class TestRSA_OAEP (unittest.TestCase):

    def setUp(self):
        now = time.time()
        self.rng = rnglib.SimpleRNG(now)
        if not os.path.exists(TEST_DIR):
            os.makedirs(TEST_DIR)

    def tearDown(self):
        pass

    def testEncryptDecrypt(self):

        # set up private RSA key, get its public part
        KEYBITS = 2048
        ckPriv = RSA.generate(KEYBITS)          # generate a 2K bit private key
        # self.assertEqual(ckPriv.size(), KEYBITS) # fails, may be a little
        # less
        ck = ckPriv.publickey()
        self.assertEqual(ck.has_private(), False)

        # prepare DecimalVersion object, get its value, an int
        w = self.rng.nextInt16(256)
        x = self.rng.nextInt16(256)
        y = self.rng.nextInt16(256)
        z = self.rng.nextInt16(256)
        versionObj = DecimalVersion(w, x, y, z)
        version = versionObj.value            # a property
        serialVersion = '%d.%d.%d.%d' % (w, x, y, z)
        versionFromS = parseDecimalVersion(serialVersion)
        self.assertEqual(version, versionFromS.value)

        # CLIENT ENCRYPTS HELLO -------------------------------------

        encryptedHello, iv1, key1, salt1 = hr.clientEncryptHello(version, ck)
        self.assertEqual(len(encryptedHello), KEYBITS / 8)
        self.assertEqual(len(iv1), hr.AES_BLOCK_SIZE)
        self.assertEqual(len(key1), 2 * hr.AES_BLOCK_SIZE)
        self.assertEqual(len(salt1), 8)

        # SERVER DECRYPTS HELLO -------------------------------------
        iv1s, key1s, salt1s, versionS = hr.serverDecryptHello(
            encryptedHello, ckPriv)

        # in real use, the server could require a different version
        self.assertEqual(versionS, version)
        self.assertEqual(iv1, iv1s)
        self.assertEqual(key1, key1s)
        self.assertEqual(salt1, salt1s)

        # SERVER PREPARES AND ENCRYPTS REPLY ------------------------
        version2s = self.rng.nextInt32()
        iv2s, key2s, salt2s, encryptedReply = hr.serverEncryptHelloReply(
            iv1, key1, salt1, version2s)

        # CLIENT DECRYPTS REPLY -------------------------------------
        iv2, key2, salt2, salt1x, version2 = hr.clientDecryptHelloReply(
            encryptedReply, iv1, key1)

        self.assertEqual(iv2, iv2s)
        self.assertEqual(key2, key2s)
        self.assertEqual(salt2, salt2s)
        self.assertEqual(salt1x, salt1)


if __name__ == '__main__':
    unittest.main()
