#!/usr/bin/env python3
# xlattice_py/test_pyca_node.py

""" Test Python3 version of the XLattice Node. """

import time
import unittest

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

from xlattice import HashTypes, UnrecognizedHashTypeError
from xlattice.pyca_node import Node
from rnglib import SimpleRNG

RNG = SimpleRNG(time.time)


class TestNode(unittest.TestCase):
    """
    Tests an XLattice-style Node, including its sign() and verify()
    functions, using SHA1 and SHA2(56)
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def check_node(self, node, hashtype):
        """
        Verify that the sk_ public key can be used for signing.
        """
        assert node is not None

        sk_ = node.sk_
        id_ = node.node_id
        # pylint:disable=redefined-variable-type
        if hashtype == HashTypes.SHA1:
            self.assertEqual(20, len(id_))
            sha = hashes.Hash(hashes.SHA1(), backend=default_backend())
        elif hashtype == HashTypes.SHA2:
            self.assertEqual(32, len(id_))
            sha = hashes.Hash(hashes.SHA256(), backend=default_backend())
        else:
            raise UnrecognizedHashTypeError("%d" % hashtype)

        pem_sk = sk_.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.PKCS1)
        sha.update(pem_sk)
        calculated_id = sha.finalize()
        self.assertEqual(id_, calculated_id)

        # make a random array of bytes
        count = 16 + RNG.next_int16(256)
        msg_ = bytearray(count)
        RNG.next_bytes(msg_)
        msg = bytes(msg_)

        # sign it and verify that it verifies
        sig = node.sign(msg)

        try:
            node.verify(msg, sig)
            # success if we get here
        except InvalidSignature:
            self.fail("unexpected InvalidSignature")

        # flip some bits and verify that it doesn't verify with the same sig
        msg_ = bytearray(msg)
        msg_[0] = msg_[0] ^ 0x36
        msg2 = bytes(msg_)
        try:
            node.verify(msg2, sig)
            self.fail("verification should have failed")
        except InvalidSignature:
            # success
            pass

    # ===============================================================

    def do_test_generate_rsa_key(self, hashtype):
        """
        Create a Node with the hash type specified; constructor creates
        the RSA key.
        """
        nnn = Node(hashtype)          # no RSA key provided, so creates one
        self.check_node(nnn, hashtype)

    def test_generated_rsa_key(self):
        """
        Create and test Nodes using a range of hash types; constructor
        creates the RSA key.

        SHA3 has been dropped.
        """
        for hashtype in [HashTypes.SHA1, HashTypes.SHA2]:
            self.do_test_generate_rsa_key(hashtype)

    # ===============================================================

    # DROPPED OpenSSL-related tests.


if __name__ == '__main__':
    unittest.main()
