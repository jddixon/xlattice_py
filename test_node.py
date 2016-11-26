#!/usr/bin/env python3

# xlattice_py/testNode.py, copied here from pzog/xlattice

import sys
import time
import unittest
import hashlib

from Crypto.PublicKey import RSA as rsa
# from Crypto.Signature import PKCS1_v1_5 as pkcs1
from xlattice import QQQ, UnrecognizedSHAError
from xlattice.node import Node
from rnglib import SimpleRNG

if sys.version_info < (3, 6):
    # pylint: disable=unused-import
    import sha3     # must follow hashlib, which it monkey-patches

RNG = SimpleRNG(time.time)


class TestNode(unittest.TestCase):
    """
    Tests an XLattice-style Node, including its sign() and verify()
    functions, using SHA1, SHA2(56), and SHA3[-256]
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def check_node(self, node, using_sha):
        assert node is not None

        pub = node.pub_key
        id_ = node.node_id
        # pylint:disable=redefined-variable-type
        if using_sha == QQQ.USING_SHA1:
            self.assertEqual(20, len(id_))
            sha = hashlib.sha1()
        elif using_sha == QQQ.USING_SHA2:
            self.assertEqual(32, len(id_))
            sha = hashlib.sha256()
        elif using_sha == QQQ.USING_SHA3:
            self.assertEqual(32, len(id_))
            sha = hashlib.sha3_256()
        else:
            raise UnrecognizedSHAError("%d" % using_sha)

        sha.update(pub.exportKey())
        expected_id = sha.digest()
        self.assertEqual(expected_id, id_)

        # make a random array of bytes
        count = 16 + RNG.next_int16(256)
        msg = bytearray(count)
        RNG.next_bytes(msg)

        # sign it and verify that it verifies
        sig = node.sign(msg)
        self.assertTrue(node.verify(msg, sig))

        # flip some bits and verify that it doesn't verify with the same sig
        msg[0] = msg[0] ^ 0x36
        self.assertFalse(node.verify(msg, sig))

    # ---------------------------------------------------------------
    def do_test_generate_rsa_key(self, using_sha):
        nnn = Node(using_sha)          # no RSA key provided, so creates one
        self.check_node(nnn, using_sha)

    def test_generated_rsa_key(self):
        for using in [QQQ.USING_SHA1, QQQ.USING_SHA2, QQQ.USING_SHA3, ]:
            self.do_test_generate_rsa_key(using)

    # ---------------------------------------------------------------
    def do_test_with_openssl_key(self, using_sha):

        # import an openSSL-generated 2048-bit key (this becomes a
        # string constant in this program)
        with open('openssl2k.pem', 'r') as file:
            pem_key = file.read()
        key = rsa.importKey(pem_key)
        assert key is not None
        self.assertTrue(key.has_private())
        nnn = Node(using_sha, key)
        self.check_node(nnn, using_sha)

        # The _RSAobj.publickey() returns a raw key.
        self.assertEqual(key.publickey().exportKey(),
                         nnn.pub_key.exportKey())

        # -----------------------------------------------------------
        # CLEAN THIS UP: node.key and node.pubKey should return
        # stringified objects, but node._privateKey and _pubKey should
        # be binary
        # -----------------------------------------------------------

    def test_with_open_ssl_key(self):
        for using in [QQQ.USING_SHA1, QQQ.USING_SHA2, QQQ.USING_SHA3, ]:
            self.do_test_with_openssl_key(using)

if __name__ == '__main__':
    unittest.main()
