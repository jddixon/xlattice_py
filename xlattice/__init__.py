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

           'HashTypes', 'UnrecognizedHashTypeError',

           'check_hashtype',
           'parse_hashtype_etc', 'fix_hashtype', 'show_hashtype_etc',

           'check_u_path',

           # XLATTICE ABSTRACTIONS
           'Context', 'ContextError', ]

__version__ = '1.7.8'
__version_date__ = '2017-02-25'


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


# ABSTRACTIONS ======================================================

"""
The XLattice Context.

"""


class ContextError(RuntimeError):
    """ Handles Context-related exceptions. """

# Any reason to make this ABCMeta ?


class Context(dict):
    """
    The XLattice context.

    A naming context consisting of a possibly nested set of name-to-object
    bindings.  If there is a parent context and a key cannot be resolved
    in this context, an attempt will be made to resolve it in the parent,
    recursively.

    Names added to the context must not be None.

    This implementation is intended to be thread-safe.
    """

    def __init__(self, parent=None):
        """ Create a Context, optionally with a parent. """
        super().__init__()
        self._parent = parent

    def synchronize(self):
        """
        TBD magic.

        This makes no sense as it is set out.
        """

    def bind(self, name, obj):        # -> Context
        """
        Bind a name to an Object at this Context level.  Neither name
        nor object may be None.

        If this context has a parent, the binding at this level will
        mask any bindings in the parent and above.

        @param name the name being bound
        @param o    the Object it is bound to
        @raises ContextError if either is None.
        """

        if name is None or obj is None:
            raise ContextError("name or object is None")
        self.synchronize()      # XXX needs to sync block
        self[name] = obj
        return self

    def lookup(self, name):          # -> object
        """
        Looks up a name recursively.  If the name is bound at this level,
        the object it is bound to is returned.  Otherwise, if there is
        a parent Context, the value returned by a lookup in the parent
        Context is returned.  If there is no parent and no match, returns
        None.

        @param name the name we are attempting to match
        @return     the value the name is bound to at this or a higher level
                    or None if there is no such value
        """
        if name is None:
            raise ContextError("name cannot be None")
        obj = None
        self.synchronize()
        if name in self:
            obj = self[name]
        elif self._parent is not None:
            obj = self._parent.lookup(name)
        return obj

    def unbind(self, name):        # -> None
        """
        Remove a binding from the Context.  If there is no such binding,
        silently ignore the request.  Any binding at a higher level, in
        the parent Context or above, is unaffected by this operation.

        @param name Name to be unbound.
        """
        self.synchronize()
        # XXX Need to sync on block
        if name is None:
            raise ContextError("name is None")
        # XXX will raise if not in dict
        del self[name]

    def size(self):                 # -> int
        """ Return the number of bindings at this level. """
        self.synchronize()          # XXX need to sync on block
        return len(self)

    @property
    def parent(self):
        """
        Return a reference to the parent Context or None if there is none.
        """
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        """
        Change the parent Context. This method returns a reference to
        this instance, to allow method calls to be chained.

        @param  new_parent New parent Context, possibly None.
        Return a reference to the current Context
        """

        self._parent = new_parent
        return self
