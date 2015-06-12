# xlattice_py/xlattice/__init__.py

import binascii

__all__ = [ '__version__',      '__version_date__',     
            'SHA1_BIN_NONE',    'SHA2_BIN_NONE',
            'SHA1_HEX_NONE',    'SHA1_B64_NONE',
            'SHA2_HEX_NONE',
        ]

__version__      = '0.1.7'
__version_date__ = '2015-06-12'


# This is the SHA1 of an empty string (or file)
                #  ....x....1....x....2....x....3....x....4
SHA1_HEX_NONE   = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'

# The same value base64
SHA1_B64_NONE   = '2jmj7l5rSw0yVb/vlWAYkK/YBwk='

# The SHA2(56) of an empty string or file
      #  ....x....1....x....2....x....3....x....4....x....5....x....6....
SHA2_HEX_NONE   = \
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

# The lengths of SHA byte arrays or hex strings respectively
SHA1_BIN_LEN    = 20
SHA1_HEX_LEN    = 40
SHA2_BIN_LEN    = 32
SHA2_HEX_LEN    = 64

# Binary values 
SHA1_BIN_NONE = binascii.a2b_hex(SHA1_HEX_NONE)
SHA2_BIN_NONE = binascii.a2b_hex(SHA2_HEX_NONE)

