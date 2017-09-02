#!/usr/bin/env python3
# xlattice_py/test_rsa.py; moved here from buildList

""" Test RSA crypto routines.  """

import base64
import os
import time
import unittest
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA    # presumably 1
from Crypto.Signature import PKCS1_PSS

from rnglib import SimpleRNG
from xlattice.crypto import XLCryptoError, collect_pem_rsa_public_key


class TestRSA(unittest.TestCase):
    """ Test RSA crypto routines.  """

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    def test_rsa_serialization(self):

        tmp_dir = 'tmp'
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)
        while True:
            sub_dir = self.rng.next_file_name(12)
            node_dir = os.path.join(tmp_dir, sub_dir)
            if not os.path.exists(node_dir):
                break
        # DEBUG
        # print("nodeDir is %s" % nodeDir)
        # END
        os.mkdir(node_dir)

        # TEST SERIALIZATIon, DESERIALIZATION OF KEYS ---------------

        # we begin with the private key in PEM (text) format
        sk_priv = RSA.generate(1024)     # cheap key for testing
        key_file = os.path.join(node_dir, 'skPriv.pem')
        with open(key_file, 'wb') as file:
            # written as bytes
            file.write(sk_priv.exportKey('PEM'))

        self.assertTrue(os.path.exists(node_dir))
        with open(key_file, 'r') as file:
            sk_priv = RSA.importKey(file.read())

        # get the public part of the key
        sk_ = sk_priv.publickey()

        # transform key into DER (binary) format
        sk_priv_der_file = os.path.join(node_dir, 'skPriv.der')
        der_data = sk_priv.exportKey('DER')
        with open(sk_priv_der_file, 'wb') as file:
            file.write(der_data)

        # write the public key in PEM format
        sk_file = os.path.join(node_dir, 'sk.pem')
        with open(sk_file, 'wb') as file:
            file.write(sk_.exportKey('PEM'))

#       # write the public key in OpenSSH format
#       # XXX THIS FAILS - bug in pycrypto ("can't concat", below)
#       o_file = os.path.join(node_dir, 'sk.openssh')
#       with open(o_file, 'w') as file:
#           # XXX POSSIBLE ValueError, which doesn't get decoded like this
#           # DEBUG ---------------------------------------
#           print('TYPE sk_: ', type(sk_))
#           # NEXT LINE gets "can't concat bytes to str"
#           stuff = sk_.exportKey('OpenSSH')
#           print("TYPE STUFF: ", type(stuff))
#           # END -----------------------------------------
#           file.write(sk_.exportKey('OpenSSH'))

        sk_priv2 = RSA.importKey(der_data)
        sk2 = sk_priv2.publickey()

        # verify that public key parts are identical
        self.assertEqual(sk_.exportKey('DER'), sk2.exportKey('DER'))

        # TEST PEM DESERIALIZATION FROM STRINGS ---------------------

        try:
            # pylint seems confused, complains ValueError has no decode member
            # pylint: disable=no-member
            pem_str = sk_.exportKey('PEM').decode('utf-8')
        except ValueError as exc:
            raise XLCryptoError(exc)

        # depth == 0 test (where depth is number of leading spaces)
        strings = pem_str.split('\n')
        string = strings[0]
        strings = strings[1:]
        pem_pk, rest = collect_pem_rsa_public_key(string, strings)
        self.assertEqual(pem_pk, pem_str)

        # depth > 0 test
        strings = pem_str.split('\n')
        tt_ = []
        depth = 1 + self.rng.next_int16(10)   # so from 1 to 10 inclusive
        indent = ' ' * depth
        for line in strings:
            tt_.append(indent + line)
        tt_.append('this is a line of junk')
        string = tt_[0][depth:]
        tt_ = tt_[1:]
        pem_pk, rest = collect_pem_rsa_public_key(string, tt_)
        self.assertEqual(pem_pk, pem_str)
        self.assertEqual(len(rest), 1)
        self.assertEqual(rest[0], 'this is a line of junk')

    def test_dig_sig(self):
        """ Test digital signatures. """

        sk_priv = RSA.generate(1024)     # cheap key for testing
        # get the public part of the key
        sk_ = sk_priv.publickey()

        count = 64 + self.rng.next_int16(192)
        data = self.rng.some_bytes(count)
        self.assertTrue(sk_priv.can_sign())
        # self.assertFalse(sk, can_sign())  # no such method

        sha = SHA.new()
        sha.update(data)
        signer = PKCS1_PSS.new(sk_priv)
        signature = signer.sign(sha)     # guess at interface ;-)

        b64sig = base64.b64encode(signature).decode('utf-8')
        # DEBUG
        # print("DIG SIG:\n%s" % b64sig)
        # END
        sig2 = base64.b64decode(b64sig)
        self.assertEqual(sig2, signature)

        sha = SHA.new()
        sha.update(data)
        verifier = PKCS1_PSS.new(sk_)
        self.assertTrue(verifier.verify(sha, signature))

        # twiddle a random byte in data array to make verification fail
        sha_2 = SHA.new()
        which = self.rng.next_int16(count)
        data[which] = 0xff & ~data[which]
        sha_2.update(data)
        self.assertFalse(verifier.verify(sha_2, signature))


if __name__ == '__main__':
    unittest.main()
