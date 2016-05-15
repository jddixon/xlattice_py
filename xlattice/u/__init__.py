# xlattice_py/xlattice/u/__init__.py

import binascii
import hashlib
import io
import os
import time
import rnglib

__all__ = ['__version__', '__version_date__',
           'SHA1_BIN_NONE', 'SHA2_BIN_NONE',
           'SHA1_HEX_NONE', 'SHA1_B64_NONE',
           'SHA2_HEX_NONE',
           # classes
           'ULock',
           # functions
           'fileSHA1Bin', 'fileSHA1Hex', 'fileSHA2Bin', 'fileSHA2Hex',
           ]

# NEED TO DECIDE WHETHER THESE BELONG HERE ######
# __version__ = '0.6.1'
# __version_date__ = '2016-05-11'
# END NEED TO DECIDE ############################

# This is the SHA1 of an empty string (or file)
#  ....x....1....x....2....x....3....x....4
SHA1_HEX_NONE = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'

# The same value base64
SHA1_B64_NONE = '2jmj7l5rSw0yVb/vlWAYkK/YBwk='

# The SHA2(56) of an empty string or file
#  ....x....1....x....2....x....3....x....4....x....5....x....6....
SHA2_HEX_NONE   = \
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

# The lengths of SHA byte arrays or hex strings respectively
SHA1_BIN_LEN = 20
SHA1_HEX_LEN = 40
SHA2_BIN_LEN = 32
SHA2_HEX_LEN = 64

# Binary values
SHA1_BIN_NONE = binascii.a2b_hex(SHA1_HEX_NONE)
SHA2_BIN_NONE = binascii.a2b_hex(SHA2_HEX_NONE)

# CONSTANTS ========================================================-

# The next line needs to be synchronized
RNG = rnglib.SimpleRNG(time.time())

# - fileSHA1 --------------------------------------------------------


def fileSHA1Bin(path):
    if path is None or not os.path.exists(path):
        return None

    d = hashlib.sha1()
    f = io.FileIO(path, 'rb')
    r = io.BufferedReader(f)
    while (True):
        byteStr = r.read(io.DEFAULT_BUFFER_SIZE)
        if (len(byteStr) == 0):
            break
        d.update(byteStr)
    r.close()
    return bytes(d.digest())    # a binary value


def fileSHA1Hex(path):
    if path is None or not os.path.exists(path):
        return None

    d = hashlib.sha1()
    f = io.FileIO(path, 'rb')
    r = io.BufferedReader(f)
    while (True):
        byteStr = r.read(io.DEFAULT_BUFFER_SIZE)
        if (len(byteStr) == 0):
            break
        d.update(byteStr)
    r.close()
    return d.hexdigest()    # a string, of course!


def fileSHA2Bin(path):
    if path is None or not os.path.exists(path):
        return None

    d = hashlib.sha256()
    f = io.FileIO(path, 'rb')
    r = io.BufferedReader(f)
    while (True):
        byteStr = r.read(io.DEFAULT_BUFFER_SIZE)
        if (len(byteStr) == 0):
            break
        d.update(byteStr)
    r.close()
    return bytes(d.digest())   # a binary value


def fileSHA2Hex(path):
    if path is None or not os.path.exists(path):
        return None

    d = hashlib.sha256()
    f = io.FileIO(path, 'rb')
    r = io.BufferedReader(f)
    while (True):
        byteStr = r.read(io.DEFAULT_BUFFER_SIZE)
        if (len(byteStr) == 0):
            break
        d.update(byteStr)
    r.close()
    return d.hexdigest()    # a string, of course!

# ulock CLASSES =====================================================


class ULock:
    # these are UNPROTECTED
    __slots__ = ['lockDir', 'lockFile', 'pid']

    def __init__(self, uDir='/var/U'):
        self.pid = os.getpid()
        absPathToU = os.path.abspath(uDir)
        self.lockDir = '/tmp/u' + absPathToU
        if (not os.path.exists(self.lockDir)):
            os.makedirs(self.lockDir)
            # KNOWN PROBLEM: we may have created several directories
            # but only the bottom one is 0777
            os.chmod(self.lockDir, 0o777)
        self.lockFile = "%s/pid" % self.lockDir

    # - getLock -------------------------------------------
    def getLock(self, verbose=False):
        """
        Try to get a lock on uDir, returning True if successful, False
        otherwise.
        """
        if (os.path.exists(self.lockFile)):
            oldPID = ''
            with open(self.lockFile, 'r') as f:
                oldPID = int(f.read())
            if verbose:
                print('%s is already locked by process %s' % (self.lockDir,
                                                              self.pid))
            return False
        else:
            with open(self.lockFile, 'w') as f:
                f.write(str(self.pid))
            return True

    # - releaseLock --------------------------------------
    def releaseLock(self):
        if (os.path.exists(self.lockFile)):
            os.remove(self.lockFile)
