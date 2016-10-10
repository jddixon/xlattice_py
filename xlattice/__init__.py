# xlattice_py/xlattice/__init__.py

import binascii
import os
import sys
from enum import IntEnum

__all__ = ['__version__', '__version_date__',
           'SHA1_BIN_NONE', 'SHA1_HEX_NONE',
           'SHA2_BIN_NONE', 'SHA2_HEX_NONE',
           'SHA3_BIN_NONE', 'SHA3_HEX_NONE',
           'SHA1_B64_NONE',
           'SHA1_BIN_LEN', 'SHA2_BIN_LEN', 'SHA3_BIN_LEN',
           'SHA1_HEX_LEN', 'SHA2_HEX_LEN', 'SHA3_HEX_LEN',
           'Q', 'UnrecognizedSHAError',

           'checkUsingSHA',
           # argparse-related: -1,-2,-3 become args.using_sha
           'parseUsingSHA', 'fixUsingSHA', 'checkUPath', 'showUsingSHA',

           # SYNONYMS
           'check_using_sha',
           'parse_using_sha', 'fix_using_sha', 'check_u_path', 'show_using_sha',
           ]

__version__ = '1.3.9'
__version_date__ = '2016-10-10'


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


class UnrecognizedSHAError(RuntimeError):
    pass


# SYNONYM
def checkUsingSHA(using):
    return check_using_sha(using)


def check_using_sha(using):
    if not using in [
            Q.USING_SHA1,
            Q.USING_SHA2,
            Q.USING_SHA3, ]:
        raise UnrecognizedSHAError('%s' % using)


# -- argParse related -----------------------------------------------

# handle -1, -2, -3, -u/--uPath,  -v/--verbose


# SYNONYM
def parseUsingSHA(parser):
    return parse_using_sha(parser)


def parse_using_sha(parser):

    parser.add_argument('-1', '--using_sha1', action='store_true',
                        help='using the 160-bit SHA1 hash')

    parser.add_argument('-2', '--using_sha2', action='store_true',
                        help='using the 256-bit SHA2 (SHA256) hash')

    parser.add_argument('-3', '--using_sha3', action='store_true',
                        help='using the 256-bit SHA3 (Keccak-256) hash')

    parser.add_argument('-u', '--u_path',
                        help='path to uDir')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='be chatty')

# SYNONYM


def fixUsingSHA(args):
    return fix_using_sha(args)


def fix_using_sha(args):
    """ assigns a value to args.using_sha """
    args.using_sha = None
    if args.using_sha1:
        args.using_sha = Q.USING_SHA1
    elif args.using_sha2:
        args.using_sha = Q.USING_SHA2
    elif args.using_sha3:
        args.using_sha = Q.USING_SHA3

# SYNONYM


def checkUPath(parser, args, mustExist=False, mode=0o755):
    return check_u_path(parser, args, mustExist, mode)


def check_u_path(parser, args, mustExist=False, mode=0o755):
    """
    Raises RunimeError if uPath is not specified; or does not exist
    whereas it must; or exists but is not a directory.
    """

    if not args.u_path:
        raise RuntimeError("uPath %s must be specified" % args.u_path)

    if args.u_path and args.u_path[-1] == '/':
        args.u_path = args.u_path[:-1]          # drop any trailing slash

    exists = os.path.exists(args.u_path)

    if mustExist and not exists:
        raise RuntimeError("uPath %s does not exist but must" % args.u_path)

    if not exists:
        os.makedirs(args.u_path, mode=mode)
    else:
        if not os.path.isdir(args.u_path):
            raise RuntimeError(
                "uPath directory %s is not a directory" % args.u_path)

# SYNONYM


def showUsingSHA(args):
    return show_using_sha(args)


def show_uing_sha(args):
    print('uPath        = ' + str(args.u_path))
    print('usingSHA     = ' + str(args.using_sha))
    print('verbose      = ' + str(args.verbose))
