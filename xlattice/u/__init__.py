# xlattice_py/xlattice/u/__init__.py

import binascii
import hashlib
import io
import os
import shutil
import time
import rnglib

__all__ = ['__version__', '__version_date__',
           'SHA1_BIN_NONE', 'SHA2_BIN_NONE',
           'SHA1_HEX_NONE', 'SHA1_B64_NONE',
           'SHA2_HEX_NONE',
           'FLAT_DIR', 'DIR16x16', 'DIR256x256',
           # classes
           'UDir', 'ULock',
           # functions
           'fileSHA1Bin', 'fileSHA1Hex', 'fileSHA2Bin', 'fileSHA2Hex',
           ]

# CONSTANTS =========================================================

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

# == HACKS ==========================================================

# The next line needs to be synchronized
RNG = rnglib.SimpleRNG(time.time())

FLAT_DIR = 0x200
DIR16x16 = 0x400
DIR256x256 = 0x800

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

# CLASSES ===========================================================


class ULock(object):
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


class UDir (object):

    def __init__(self, uPath, dirStruc, usingSHA1=True):

        self._uPath = uPath
        self._dirStruc = dirStruc
        self._usingSHA1 = usingSHA1

        os.makedirs(self._uPath, mode=0o755, exist_ok=True)

        self._inDir = os.path.join(uPath, 'in')
        os.makedirs(self._inDir, mode=0o755, exist_ok=True)
        self._tmpDir = os.path.join(uPath, 'tmp')
        os.makedirs(self._tmpDir, mode=0o755, exist_ok=True)

    @property
    def dirStruc(self): return self._dirStruc

    @property
    def uPath(self): return self._uPath

    @property
    def usingSHA1(self): return self._usingSHA1

    def copyAndPut(self, path, key):
        """
        Make a local copy of the file at path and with the content key
        specified, then move the file into U.  Return the length of the
        file and its actual content key.
        """

        # CHECK KEY LENGTH

        # RACE CONDITION
        tmpFileName = os.path.join(self._tmpDir, RNG.nextFileName(16))
        while os.path.exists(tmpFileName):
            tmpFileName = os.path.join(self._tmpDir, RNG.nextFileName(16))
        shutil.copyfile(path, tmpFileName)
        return self.put(tmpFileName, key)

    def getData(self, key):
        """
        If there is a file in the store with the content key specified,
        return it.  Otherwise return None.

        XXX The file must fit in memory.
        """
        path = self.getPathForKey(key)
        if not os.path.exists(path):
            return None
        else:
            with open(path, 'rb') as f:
                data = f.read()
            return data

    def put(self, inFile, key):
        """
        inFile is the path to a local file which will be renamed into U (or
        deleted if it is already present in U) key is an sha1 or sha256
        content hash.  If the operation succeeds we return a 2-tuple
        containing the length of the file, which must not be zero, and its
        hash.  Otherwise we return (0, '').
        """

        # CHECK KEY LENGTH

        if self._usingSHA1:
            hash = fileSHA1Hex(inFile)
        else:
            hash = fileSHA1Hex(inFile)
        if (hash != key):
            # THIS MUST BE EXCEPTION
            print("expected %s to have key %s, but the content key is %s" % (
                inFile, key, hash))
            return (0, '')
        length = os.stat(inFile).st_size

        if self.dirStruc == FLAT_DIR:
            fullishPath = os.path.join(self.uPath, key)
        else:
            if self.dirStruc == DIR16x16:
                topSubDir = hash[0]
                lowerDir = hash[1]
            elif self.dirStruc == DIR256x256:
                topSubDir = hash[0:2]
                lowerDir = hash[2:4]
            else:
                raise RuntimeError("unknown dirStruc 0x%x" % self.dirStruc)
            targetDir = self.uPath + '/' + topSubDir + '/' + lowerDir + '/'
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            fullishPath = targetDir + key

        if (os.path.exists(fullishPath)):
            os.unlink(inFile)
        else:
            shutil.move(inFile, fullishPath)
            os.chmod(fullishPath, 0o444)
        return (length, hash)

    def putData(self, data, key):
        s = hashlib.sha1()
        s.update(data)
        hash = s.hexdigest()
        if (hash != key):
            print("expected data to have key %s, but the content key is %s" % (
                key, hash))
            return (0, '')          # length and hash
        length = len(data)

        if self.dirStruc == FLAT_DIR:
            fullishPath = os.path.join(self.uPath, key)
        else:
            if self.dirStruc == DIR16x16:
                topSubDir = hash[0]
                lowerDir = hash[1]
            elif self.dirStruc == DIR256x256:
                topSubDir = hash[0:2]
                lowerDir = hash[2:4]
            else:
                raise RuntimeError("undefined dirStruc 0x%x" % self.dirStruc)

            targetDir = self.uPath + '/' + topSubDir + '/' + lowerDir + '/'
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            fullishPath = targetDir + key

        if (os.path.exists(fullishPath)):
            # print "DEBUG: file is already present"
            pass
        else:
            with open(fullishPath, 'wb') as f:
                f.write(data)
        return (length, hash)               # GEEP2

    def exists(self, key):

        # CHECK KEY LEN

        path = self.getPathForKey(key)
        return os.path.exists(path)

    def fileLen(self, key):
        """
        returns the length of the file with the given content key
        """

        # CHECK KEY LEN

        path = self.getPathForKey(key)
        return os.stat(path).st_size

    def getPathForKey(self, key):
        """
        returns a path to a file with the content key passed, or None if
        there is no such file
        """
        if self.dirStruc == FLAT_DIR:
            return os.path.join(self.uPath, key)

        if self.dirStruc == DIR16x16:
            topSubDir = key[0]
            lowerDir = key[1]
        elif self.dirStruc == DIR256x256:
            topSubDir = key[0:2]
            lowerDir = key[2:4]
        else:
            raise RuntimeError("unexpected dirStruc 0x%x" % self.dirStruc)

        return self.uPath + '/' + topSubDir + '/' + lowerDir + '/' + key
