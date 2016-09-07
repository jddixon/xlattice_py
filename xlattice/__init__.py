# xlattice_py/xlattice/__init__.py

import binascii
from enum import IntEnum

__all__ = ['__version__', '__version_date__',
           'SHA1_BIN_NONE', 'SHA1_HEX_NONE',
           'SHA2_BIN_NONE', 'SHA2_HEX_NONE',
           'SHA3_BIN_NONE', 'SHA3_HEX_NONE',
           'SHA1_B64_NONE',
           'SHA1_BIN_LEN', 'SHA2_BIN_LEN', 'SHA3_BIN_LEN',
           'SHA1_HEX_LEN', 'SHA2_HEX_LEN', 'SHA3_HEX_LEN',
           ]

__version__ = '1.3.3'
__version_date__ = '2016-09-06'


# This is the SHA1 of an empty string (or file)
#  ....x....1....x....2....x....3....x....4
SHA1_HEX_NONE = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'

# The same value base64
SHA1_B64_NONE = '2jmj7l5rSw0yVb/vlWAYkK/YBwk='

# The SHA2(56) of an empty string or file
#  ....x....1....x....2....x....3....x....4....x....5....x....6....
SHA2_HEX_NONE   = \
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

# The SHA3(256) of an empty string or file
#  ....x....1....x....2....x....3....x....4....x....5....x....6....
SHA3_HEX_NONE   = \
    'a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a'

# The lengths of SHA byte arrays or hex strings respectively
SHA1_BIN_LEN = 20
SHA1_HEX_LEN = 40

SHA2_BIN_LEN = 32
SHA2_HEX_LEN = 64

SHA3_BIN_LEN = 32
SHA3_HEX_LEN = 64

# Binary values
SHA1_BIN_NONE = binascii.a2b_hex(SHA1_HEX_NONE)
SHA2_BIN_NONE = binascii.a2b_hex(SHA2_HEX_NONE)
SHA3_BIN_NONE = binascii.a2b_hex(SHA3_HEX_NONE)


class Q (IntEnum):
    USING_SHA1 = 1
    USING_SHA2 = 2
    USING_SHA3 = 3
