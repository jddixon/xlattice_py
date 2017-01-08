#!/usr/bin/env python3

# xlattice_py/test_pyca_node.py

########################################
# BEING HACKED TO USED pyca/cryptography
########################################

import sys
import time
import unittest

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

from xlattice import QQQ, UnrecognizedSHAError
from xlattice.pyca_node import Node
from rnglib import SimpleRNG

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
            sha = hashes.Hash(hashes.SHA1(), backend=default_backend())
        elif using_sha == QQQ.USING_SHA2:
            self.assertEqual(32, len(id_))
            sha = hashes.Hash(hashes.SHA256(), backend=default_backend())
        else:
            raise UnrecognizedSHAError("%d" % using_sha)

        pem_pub = pub.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.PKCS1)
        sha.update(pem_pub)
        expected_id = sha.finalize()
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

    # ===============================================================

    def do_test_generate_rsa_key(self, using_sha):
        """
        Create a Node with the hash type specified; constructor creates
        the RSA key.
        """
        nnn = Node(using_sha)          # no RSA key provided, so creates one
        self.check_node(nnn, using_sha)

    def test_generated_rsa_key(self):
        """
        Create and test Nodes using a range of hash types; constructor
        creates the RSA key.

        SHA3 has been dropped.
        """
        for using in [QQQ.USING_SHA1, QQQ.USING_SHA2, ]:
            self.do_test_generate_rsa_key(using)

    # ===============================================================

#   def do_test_with_openssl_key(self, using_sha):

#       # import an openSSL-generated 2048-bit key (this becomes a
#       # string constant in this program)
#       with open('openssl2k.pem', 'r') as file:
#           pem_key = file.read()
#       key = rsa.importKey(pem_key)
#       assert key is not None
#       self.assertTrue(key.has_private())
#       nnn = Node(using_sha, key)
#       self.check_node(nnn, using_sha)

#       pem_pub = key.public_key.public_bytes(
#           encoding=serialization.Encoding.PEM,
#           format=serialization.PublicFormat.PKCS1)

#       self.assertEqual(key.public_key().exportKey(),
#                        nnn.pub_key.exportKey())

#       # -----------------------------------------------------------
#       # CLEAN THIS UP: node.key and node.pubKey should return
#       # stringified objects, but node._privateKey and _pubKey should
#       # be binary
#       # -----------------------------------------------------------

#   def test_with_open_ssl_key(self):
#       # SHA3 is dropped
#       for using in [QQQ.USING_SHA1, QQQ.USING_SHA2, ]:
#           self.do_test_with_openssl_key(using)

if __name__ == '__main__':
    unittest.main()
