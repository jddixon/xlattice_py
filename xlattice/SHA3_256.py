#~/dev/py/xlattice_py/SHA3_256.py

"""SHA3_256 cryptographic hash algorithm.

SHA3_256 produces a 256-bit digest of a message.

    >>> from pzog.xlattice import SHA3_256
    >>>
    >>> h = SHA3_256.new()
    >>> h.update(b'Hello')
    >>> print h.hexdigest()

"""

__all__ = ['new', 'digest_size', 'SHA3_256Hash']

from Crypto.Util.py3compat import *
from Crypto.Hash.hashalgo import HashAlgo

import hashlib
import sys
if sys.version_info < (3, 4):
    import sha3                 # first import patches hashlib

hashFactory = hashlib.sha3_256


class SHA3_256Hash(HashAlgo):
    """Class that implements a SHA3_256 hash

    :undocumented: block_size
    """

    # ASN.1 object identifier (OID).  This is a private identifier,
    # 1.3.6.1.4.1.0.1.  The encoded OID is then
    #       06                              # OID
    #       07                              # LEN
    #       2b 06 01 04 01 00 01            # value, 2b being 40*1 + 3

    #: This value uniquely identifies the SHA3_256 algorithm.
    oid = b('\x06\x07\x2b\x06\x01\x04\x01\x00\x01')

    digest_size = 32
    block_size = 200   # 1600 bits

    def __init__(self, data=None):
        HashAlgo.__init__(self, hashFactory, data)

    def new(self, data=None):
        return SHA3_256Hash(data)


def new(data=None):
    """Return a fresh instance of the hash object.

    :Parameters:
       data : byte string
        The very first chunk of the message to hash.
        It is equivalent to an early call to `SHA3_256Hash.update()`.
        Optional.

    :Return: A `SHA3_256Hash` object
    """
    return SHA3_256Hash().new(data)

#: The size of the resulting hash in bytes.
digest_size = SHA3_256Hash.digest_size

#: The internal block size of the hash algorithm in bytes.
block_size = SHA3_256Hash.block_size
