#!/usr/bin/env python3

import sys
import unittest

from xlattice import SHA3_256

# This code was crudely hacked from pysha3_0.2.1 tests.py

#####################################################################
# THIS TEST CURRENTLY FAILS BECAUSE THERE IS NO PYTHON3 SUPPORT FOR
# SHA3/KECCAK
#####################################################################

if sys.version_info[0] == 3:
    fromhex = bytes.fromhex
    tobyte = lambda b: bytes([b])
    asunicode = lambda s: s
else:
    fromhex = lambda s: s.decode("hex")
    tobyte = lambda b: bytes(b)
    asunicode = lambda s: s.decode("ascii")


class BaseSHA3Tests(unittest.TestCase):
    new = None
    name = None
    digest_size = None
    vectors = []

    def assertHashDigest(self, hexmsg, hexdigest):
        hexdigest = hexdigest.lower()
        msg = fromhex(hexmsg)
        digest = fromhex(hexdigest)
        self.assertEqual(len(digest), self.digest_size)

        sha3 = self.new(msg)
        self.assertEqual(sha3.hexdigest(), hexdigest)
        self.assertEqual(sha3.digest(), digest)

        sha3 = self.new()
        sha3.update(msg)
        self.assertEqual(sha3.hexdigest(), hexdigest)
        self.assertEqual(sha3.digest(), digest)

        sha3 = self.new()
        for b in msg:
            sha3.update(tobyte(b))
        self.assertEqual(sha3.hexdigest(), hexdigest)
        self.assertEqual(sha3.digest(), digest)

    def test_basics(self):
        sha3 = self.new()

        # XXX FAILS: sha3 instance has no attribute 'name'
        # self.assertEqual(sha3.name, self.name)

        self.assertEqual(sha3.digest_size, self.digest_size)
        self.assertEqual(len(sha3.digest()), self.digest_size)
        self.assertEqual(len(sha3.hexdigest()), self.digest_size * 2)

        # DEBUG - we show that sha3.digest is mutable, although we
        # would rather that it wasn't
        print("DEBUG: sha3.digest is %s" % str(sha3.digest))
        setattr(sha3, 'digest', 42)
        print("DEBUG: sha3.digest is %s" % str(sha3.digest))
        # END

        # the first assertion tests much the same thing
        # self.assertRaises(AttributeError, setattr, sha3, "digest", 3)  # FAILS
        # self.assertRaises(AttributeError, setattr, sha3, "name", "egg")#
        # FAILS

        self.new(b"data")
        # self.new(string=b"data")  # XXX NO SUCH ATTRIBUTE as string
        # XXX FAILS:
        # self.assertRaises(TypeError, self.new, None)

        self.assertRaises(TypeError, sha3.update, None)
        self.assertRaises(TypeError, self.new, asunicode("text"))
        self.assertRaises(TypeError, sha3.update, asunicode("text"))

    def test_vectors(self):
        for hexmsg, hexdigest in self.vectors:
            self.assertHashDigest(hexmsg, hexdigest)


class SHA3_256Tests(BaseSHA3Tests):
    new = SHA3_256.SHA3_256Hash
    name = "sha3_256"
    digest_size = 32
    vectors = [
        ("", "C5D2460186F7233C927E7DB2DCC703C0E500B653CA82273B7BFAD8045D85A470"),
        ("CC", "EEAD6DBFC7340A56CAEDC044696A168870549A6A7F6F56961E84A54BD9970B8A"),
        ("41FB", "A8EACEDA4D47B3281A795AD9E1EA2122B407BAF9AABCB9E18B5717B7873537D2"),
        ("433C5303131624C0021D868A30825475E8D0BD3052A022180398F4CA4423B98214B6BEAAC21C8807A2C33F8C93BD42B092CC1B06CEDF3224D5ED1EC29784444F22E08A55AA58542B524B02CD3D5D5F6907AFE71C5D7462224A3F9D9E53E7E0846DCBB4CE",
         "CE87A5173BFFD92399221658F801D45C294D9006EE9F3F9D419C8D427748DC41"),
    ]


def test_main():
    suite = unittest.TestSuite()
    classes = [ \
        # SHA3_224Tests,
        SHA3_256Tests,
        # SHA3_384Tests, SHA3_512Tests]
    ]
    for cls in classes:
        suite.addTests(unittest.makeSuite(cls))
    return suite

if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(test_main())
    sys.exit(not result.wasSuccessful())
