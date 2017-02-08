# xlattice_py/xlattice/__init__.py

""" XLattice library implementation for Python3. """

import binascii
import os
import sys
import warnings
from enum import IntEnum

__all__ = ['__version__', '__version_date__',
           'SHA1_BIN_NONE', 'SHA1_HEX_NONE',
           'SHA2_BIN_NONE', 'SHA2_HEX_NONE',
           'SHA3_BIN_NONE', 'SHA3_HEX_NONE',
           'SHA1_B64_NONE',
           'SHA1_BIN_LEN', 'SHA2_BIN_LEN', 'SHA3_BIN_LEN',
           'SHA1_HEX_LEN', 'SHA2_HEX_LEN', 'SHA3_HEX_LEN',

           # DEPRECATED
           # DROP ON REACHING v1.7 **********************************
           'Q', 'QQQ', 'UnrecognizedSHAError',
           # END DEPRECATED

           'HashTypes', 'UnrecognizedHashTypeError',

           # SYNONYMS -----------------------------------------------
           # DROP ON REACHING v1.7 **********************************
           'checkUsingSHA',
           #  argparse-related: -1,-2,-3 become args.using_sha
           'parseUsingSHA', 'fixUsingSHA', 'checkUPath', 'showUsingSHA',
           # END SYN ------------------------------------------------

           # BEING RENAMED, SO DEPRECATED ---------------------------
           # DROP ON REACHING v1.7 **********************************
           'check_using_sha',
           'parse_using_sha', 'fix_using_sha', 'show_using_sha',
           # END BEING RENAMED --------------------------------------
           'check_hashtype',
           'parse_hashtype_etc', 'fix_hashtype', 'show_hashtype_etc',

           'check_u_path', ]

__version__ = '1.6.7'
__version_date__ = '2017-02-07'


# This is the SHA1 of an empty string (or file)
#                ....x....1....x....2....x....3....x....4
SHA1_HEX_NONE = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'

# The same value base64
SHA1_B64_NONE = '2jmj7l5rSw0yVb/vlWAYkK/YBwk='

# The SHA2(56) of an empty string or file
#    ....x....1....x....2....x....3....x....4....x....5....x....6....
SHA2_HEX_NONE =\
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

# The SHA3(256) of an empty string or file
#    ....x....1....x....2....x....3....x....4....x....5....x....6....
SHA3_HEX_NONE =\
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

# DEPRECATED --------------------------------------------------------
# DROP ON REACHING v1.7 *********************************************


class Q(IntEnum):
    """
    SHA hash types in use.

    Deprecated: name lengthened to QQQ, then replaced by HashTypes class.
    """
    USING_SHA1 = 1
    USING_SHA2 = 2
    USING_SHA3 = 3
    warnings.warn('Q synonym', DeprecationWarning)


class QQQ(IntEnum):
    """
    SHA hash types in use.

    Deprecated: replaced by HashTypes class.
    """
    USING_SHA1 = 1
    USING_SHA2 = 2
    USING_SHA3 = 3
    warnings.warn('QQQ synonym', DeprecationWarning)


class UnrecognizedSHAError(RuntimeError):
    """ Raised if a hash type is not in QQQ's standard list. """
    warnings.warn('UnrecognizedSHAError synonym', DeprecationWarning)
    pass


# END DEPRECATED ------------------------------------------


class HashTypes(IntEnum):
    """ Hash types in use.  """
    SHA1 = 1
    SHA2 = 2
    SHA3 = 3


class UnrecognizedHashTypeError(RuntimeError):
    """ Raised if a hash type is not in HashTypes's standard list. """
    pass


# -- argParse related -----------------------------------------------

# handle -1, -2, -3, -u/--u_path,  -v/--verbose


# DEPRECATED ========================================================
# DROP ON REACHING v1.7 *********************************************

def check_using_sha(using=None):
    """
    Exit with an error message if this hash type is not supported.

    `using` is the value of a member of the HashTypes enumeration.
    """

    print('%s :: check_using_sha' % sys.argv[0], file=sys.stderr)
    warnings.warn('check_using_sha synonym', DeprecationWarning)
    if using is None:
        print("you must select -1, -2, or -3 for the sha type")
        sys.exit(1)

    if not using in [_.value for _ in QQQ]:
        raise UnrecognizedSHAError('%s' % using)


def parse_using_sha(parser):
    """ Standard arguments selecting supported hash types. """

    warnings.warn('parse_using_sha', DeprecationWarning)
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


def fix_using_sha(args):
    """
    Creates and assigns a value to args.using_sha.

    That value is determined by examining the three options
    using_sha{1,2,3}; these are then removed from the set of options.
    """
    warnings.warn('fix_usin_sha', DeprecationWarning)
    args.using_sha = None
    # pylint:disable=redefined-variable-type
    if args.using_sha1:
        args.using_sha = QQQ.USING_SHA1
    elif args.using_sha2:
        args.using_sha = QQQ.USING_SHA2
    elif args.using_sha3:
        args.using_sha = QQQ.USING_SHA3
    args.__delattr__('using_sha1')
    args.__delattr__('using_sha2')
    args.__delattr__('using_sha3')


def show_using_sha(args):
    """ Print out option values relating to SHA type, etc. """

    warnings.warn('show_using_sha', DeprecationWarning)
    print('u_path               = ' + str(args.u_path))
    print('using_sha            = ' + str(args.using_sha))
    print('verbose              = ' + str(args.verbose))

# END DEPRECATED ====================================================

# NEW HASH_TYPES CODE ========================================================


def check_hashtype(hashtype=None):
    """
    Raise if this hash type is not supported.

    Here hashtype is an integer; we check that it is in range.
    """

    if hashtype is None:
        print("you must select -1, -2, or -3 for the hash type")
        sys.exit(1)

    if not isinstance(hashtype, HashTypes):
        raise UnrecognizedHashTypeError('%s' % hashtype)


def parse_hashtype_etc(parser):
    """
    Standard arguments selecting supported hash types plus -u and -v.
    """
    parser.add_argument('-1', '--hashtype1', action='store_true',
                        help='using the 160-bit SHA1 hash')

    parser.add_argument('-2', '--hashtype2', action='store_true',
                        help='using the 256-bit SHA2 (SHA256) hash')

    parser.add_argument('-3', '--hashtype3', action='store_true',
                        help='using the 256-bit SHA3 (Keccak-256) hash')

    parser.add_argument('-u', '--u_path',
                        help='path to uDir')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='be chatty')


def fix_hashtype(args):
    """
    Creates and assigns a value to args.hashtype.

    That value is determined by examining the three options
    hashtype{1,2,3}; these are then removed from the set of options.
    """
    args.hashtype = None
    # pylint:disable=redefined-variable-type
    if args.hashtype1:
        args.hashtype = HashTypes.SHA1
    elif args.hashtype2:
        args.hashtype = HashTypes.SHA2
    elif args.hashtype3:
        args.hashtype = HashTypes.SHA3
    args.__delattr__('hashtype1')
    args.__delattr__('hashtype2')
    args.__delattr__('hashtype3')


def show_hashtype_etc(args):
    """ Print out option values relating to SHA type, etc. """
    print('hashtype             = ' + str(args.hashtype))
    print('u_path               = ' + str(args.u_path))
    print('verbose              = ' + str(args.verbose))

# END NEW HASH_TYPES CODE ===========================================


def check_u_path(parser, args, must_exist=False, mode=0o755):
    """
    Raises RunimeError if u_path is not specified; or does not exist
    whereas it must; or exists but is not a directory.
    """

    if not args.u_path:
        raise RuntimeError("u_path %s must be specified" % args.u_path)

    if args.u_path and args.u_path[-1] == '/':
        args.u_path = args.u_path[:-1]          # drop any trailing slash

    exists = os.path.exists(args.u_path)

    if must_exist and not exists:
        raise RuntimeError("u_path %s does not exist but must" % args.u_path)

    if not exists:
        os.makedirs(args.u_path, mode=mode)
    else:
        if not os.path.isdir(args.u_path):
            raise RuntimeError(
                "u_path directory %s is not a directory" % args.u_path)


# SYNONYM -----------------------------------------------------------
# DROP ON REACHING v1.7 *********************************************

def checkUsingSHA(using):
    """ SYNONYM """
    warnings.warn('checkUsingSHA synonym', DeprecationWarning)
    return check_using_sha(using)
#
#


def checkUPath(parser, args, must_exist=False, mode=0o755):
    """ SYNONYM """
    warnings.warn('checkUPath synonym', DeprecationWarning)
    return check_u_path(parser, args, must_exist, mode)
#
#


def fixUsingSHA(args):
    """ SYNONYM """
    warnings.warn('fixUsingSHA synonym', DeprecationWarning)
    return fix_using_sha(args)
#
#


def parseUsingSHA(parser):
    """ SYNONYM """
    warnings.warn('parseUsingSHA synonym', DeprecationWarning)
    return parse_using_sha(parser)
#
#


def showUsingSHA(args):
    """ SYNONYM """
    warnings.warn('showUsingSHA synonym', DeprecationWarning)
    return show_using_sha(args)
#
# END SYN -----------------------------------------------------------
