#!/usr/bin/env python3

# xlattice_py/testNode.py, copied here from pzog/xlattice

import hashlib
import sha3     # must follow hashlib import

import os
import sys
import time
import unittest

from Crypto.Hash import SHA as sha
from Crypto.PublicKey import RSA as rsa
from Crypto.Signature import PKCS1_v1_5 as pkcs1

from xlattice import Q, UnrecognizedSHAError
from xlattice.node import AbstractNode, Node, Peer
from rnglib import SimpleRNG

rng = SimpleRNG(time.time)


class TestNode (unittest.TestCase):
    """
    Tests an XLattice-style Node, including its sign() and verify()
    functions, using SHA1, SHA2(56), and SHA3[-256]
    """

    def setUp(self): pass

    def tearDown(self): pass

    def checkNode(self, node, using_sha):
        assert node is not None

        pub = node.pub_key
        id = node.node_id
        if using_sha == Q.USING_SHA1:
            self.assertEqual(20, len(id))
            dVal = hashlib.sha1()
        elif using_sha == Q.USING_SHA2:
            self.assertEqual(32, len(id))
            dVal = hashlib.sha256()
        elif using_sha == Q.USING_SHA3:
            self.assertEqual(32, len(id))
            dVal = hashlib.sha3_256()
        else:
            raise UnrecognizedSHAError("%d" % using_sha)

        dVal.update(pub.exportKey())
        expectedID = dVal.digest()
        self.assertEqual(expectedID, id)

        # make a random array of bytes
        count = 16 + rng.nextInt16(256)
        msg = bytearray(count)
        rng.nextBytes(msg)

        # sign it and verify that it verifies
        sig = node.sign(msg)
        self.assertTrue(node.verify(msg, sig))

        # flip some bits and verify that it doesn't verify with the same sig
        msg[0] = msg[0] ^ 0x36
        self.assertFalse(node.verify(msg, sig))

    # ---------------------------------------------------------------
    def doTestGenerateRSAKey(self, using_sha):
        n = Node(using_sha)          # no RSA key provided, so creates one
        self.checkNode(n, using_sha)

    def testGeneratedRSAKey(self):
        for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3, ]:
            self.doTestGenerateRSAKey(using)

    # ---------------------------------------------------------------
    def doTestWithOpenSSLKey(self, using_sha):

        # import an openSSL-generated 2048-bit key (this becomes a
        # string constant in this program)
        with open('openssl2k.pem', 'r') as file:
            pemKey = file.read()
        key = rsa.importKey(pemKey)
        assert key is not None
        self.assertTrue(key.has_private())
        n = Node(using_sha, key)
        self.checkNode(n, using_sha)

        # The _RSAobj.publickey() returns a raw key.
        self.assertEqual(key.publickey().exportKey(),
                         n.pub_key.exportKey())

        # -----------------------------------------------------------
        # CLEAN THIS UP: node.key and node.pubKey should return
        # stringified objects, but node._privateKey and _pubKey should
        # be binary
        # -----------------------------------------------------------

    def testWithOpenSSLKey(self):
        for using in [Q.USING_SHA1, Q.USING_SHA2, Q.USING_SHA3, ]:
            self.doTestWithOpenSSLKey(using)

if __name__ == '__main__':
    unittest.main()
