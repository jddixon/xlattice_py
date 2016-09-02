# xlattice_py/xlattice/u/__init__.py

import binascii
import hashlib
import io
import os
import re
import shutil
import time
import rnglib

from xlattice import Q

__all__ = ['__version__', '__version_date__',
           'SHA1_BIN_NONE', 'SHA2_BIN_NONE',
           'SHA1_HEX_NONE', 'SHA1_B64_NONE',
           'SHA2_HEX_NONE',
           'DIR_STRUC_NAMES',

           # classes
           'UDir', 'ULock',
           'XLUError',
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


class XLUError(RuntimeError):
    pass


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

    DIR_FLAT = 0
    DIR16x16 = 1
    DIR256x256 = 2
    DIR_STRUC_MAX = 3

    DIR_STRUC_NAMES = ['DIR_FLAT', 'DIR16x16', 'DIR256x256', ]

    HEX_FILE_NAME_1_PAT = r'^[0-9a-fA-F]{40}$'
    HEX_FILE_NAME_2_PAT = r'^[0-9a-fA-F]{64}$'

    HEX_DIR_NAME_16_PAT = r'^[0-9a-fA-F]{1}$'    # single hex digit
    HEX_DIR_NAME_256_PAT = r'^[0-9a-fA-F]{2}$'   # two hex digits

    HEX_FILE_NAME_1_RE = re.compile(HEX_FILE_NAME_1_PAT)
    HEX_FILE_NAME_2_RE = re.compile(HEX_FILE_NAME_2_PAT)

    HEX_DIR_NAME_16_RE = re.compile(HEX_DIR_NAME_16_PAT)
    HEX_DIR_NAME_256_RE = re.compile(HEX_DIR_NAME_256_PAT)

    _nameToDirStruc = {
        'DIR_FLAT': DIR_FLAT,
        'DIR16x16': DIR16x16,
        'DIR256x256': DIR256x256,
    }

    def nameToDirStruc(s):
        """ map a string into an integer"""
        return UDir._nameToDirStruc[s]

    _dirStrucToName = {
        DIR_FLAT: 'DIR_FLAT',
        DIR16x16: 'DIR16x16',
        DIR256x256: 'DIR256x256',
    }

    def dirStrucToName(n):
        """ map an integer into a string """
        return UDir._dirStrucToName[n]

    def dirStrucSig(uPath, dirStruc, usingSHA):
        """ signatures differentiating different types of directories """
        if usingSHA == Q.USING_SHA1:
            none = SHA1_HEX_NONE
        elif usingSHA == Q.USING_SHA2:
            none = SHA2_HEX_NONE
        elif usingSHA == Q.USING_SHA3:
            none = SHA3_HEX_NONE
        if dirStruc == UDir.DIR_FLAT:
            sig = os.path.join(uPath, none)
        elif dirStruc == UDir.DIR16x16:
            sig = os.path.join(uPath,
                               os.path.join(none[0],
                                            os.path.join(none[1], none)))
        elif dirStruc == UDir.DIR256x256:
            sig = os.path.join(uPath,
                               os.path.join(none[0:2],
                                            os.path.join(none[2:4], none)))
        else:
            raise XLUError('invalid dirStruc %d' % dirStruc)

        return sig

    def __init__(self, uPath, dirStruc=DIR_FLAT, usingSHA=True, mode=0o755):

        self._uPath = uPath
        self._dirStruc = dirStruc
        self._usingSHA = usingSHA

        os.makedirs(self._uPath, mode=mode, exist_ok=True)

        # simplistic aids to discovery

        if usingSHA == Q.USING_SHA1:
            # FIX ME FIX ME FIX ME
            pathToSig = self.getPathForKey(SHA1_HEX_NONE)
        elif usingSHA == Q.USING_SHA2:
            pathToSig = self.getPathForKey(SHA2_HEX_NONE)
        elif usingSHA == Q.USING_SHA3:
            pathToSig = self.getPathForKey(SHA3_HEX_NONE)
        sigBase = os.path.dirname(pathToSig)
        os.makedirs(sigBase, exist_ok=True)
        open(pathToSig, 'a').close()                # touch

        self._inDir = os.path.join(uPath, 'in')
        os.makedirs(self._inDir, mode=mode, exist_ok=True)
        self._tmpDir = os.path.join(uPath, 'tmp')
        os.makedirs(self._tmpDir, mode=mode, exist_ok=True)

    @property
    def dirStruc(self): return self._dirStruc

    @property
    def uPath(self): return self._uPath

    @property
    def usingSHA(self): return self._usingSHA

    @classmethod
    def discover(clz, uPath, dirStruc=DIR_FLAT, usingSHA=True, mode=0o755):
        """
        If there is a directory at the expected path, return an
        appropriate tree with the directory structure found.  Otherwise
        create a directory with the characteristics suggested by the
        parameters.

        When a directory tree is created we write NONE into the tree
        as an aid to discovery.  If this is SHA1_HEX_NONE, for example,
        we discover that usingSHA is True.  If NONE is in the top
        directory, the directory structure is DIR_FLAT.  If its first
        byte is in the top directory, dirStruc is DIR16x16.  If its
        first two bytes are there, it is DIR256x256.
        """

        if os.path.exists(uPath):
            found = False

            if not found:
                flatPathTrue = os.path.join(uPath, SHA1_HEX_NONE)
                if os.path.exists(flatPathTrue):
                    found = True
                    dirStruc = UDir.DIR_FLAT
                    usingSHA = True
            if not found:
                flatPathFalse = os.path.join(uPath, SHA2_HEX_NONE)
                if os.path.exists(flatPathFalse):
                    found = True
                    dirStruc = UDir.DIR_FLAT
                    usingSHA = False

            if not found:
                dir16PathTrue = os.path.join(uPath,
                                             os.path.join(SHA1_HEX_NONE[0],
                                                          os.path.join(SHA1_HEX_NONE[1], SHA1_HEX_NONE)))
                if os.path.exists(dir16PathTrue):
                    found = True
                    dirStruc = UDir.DIR16x16
                    usingSHA = True
            if not found:
                dir16PathFalse = os.path.join(uPath,
                                              os.path.join(SHA2_HEX_NONE[0],
                                                           os.path.join(SHA2_HEX_NONE[1], SHA2_HEX_NONE)))
                if os.path.exists(dir16PathFalse):
                    found = True
                    dirStruc = UDir.DIR16x16
                    usingSHA = False

            if not found:
                dir256PathTrue = os.path.join(uPath,
                                              os.path.join(SHA1_HEX_NONE[0:2],
                                                           os.path.join(SHA1_HEX_NONE[2:4],
                                                                        SHA1_HEX_NONE)))
                if os.path.exists(dir256PathTrue):
                    found = True
                    dirStruc = UDir.DIR256x256
                    usingSHA = True
            if not found:
                dir256PathFalse = os.path.join(uPath,
                                               os.path.join(SHA2_HEX_NONE[0:2],
                                                            os.path.join(SHA2_HEX_NONE[2:4],
                                                                         SHA2_HEX_NONE)))
                if os.path.exists(dir256PathFalse):
                    found = True
                    dirStruc = UDir.DIR256x256
                    usingSHA = False

        # if uDir does not already exist, this creates it
        obj = clz(uPath, dirStruc, usingSHA, mode)
        return obj

    def copyAndPut(self, path, key):
        """
        Make a local copy of the file at path and with the content key
        specified, then move the file into U.  Return the length of the
        file and its actual content key.
        """

        # XXX we do two such stats on this file
        actualLength = os.stat(path).st_size

        # RACE CONDITION
        tmpFileName = os.path.join(self._tmpDir, RNG.nextFileName(16))
        while os.path.exists(tmpFileName):
            tmpFileName = os.path.join(self._tmpDir, RNG.nextFileName(16))

        shutil.copyfile(path, tmpFileName)
        length, hash = self.put(tmpFileName, key)

        # integrity check
        if length != actualLength:
            print("put of %s: actual length %d, returned length %d" % (
                path, actualLength, lenght))

        # DEBUG - DO NOT REMOVE THIS CASUALLY =======================
        if hash != key or path.endswith('uildList') or path.endswith('builds'):
            print('putting %s\n\tkey  %s\n\thash %s' % (path, key, hash))
        # END =======================================================

        return length, hash

    def delete(self, key):
        """
        If there is a file in the store with the hexadecimal content key
        specified, delete it and return True.  Otherwise return False.

        """
        path = self.getPathForKey(key)
        if not os.path.exists(path):
            return False
        else:
            os.unlink(path)
            return True

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

        keyLen = len(key)
        errMsg = ''
        if self.usingSHA == Q.USING_SHA1 and keyLen != SHA1_HEX_LEN:
            errMsg = "UDir.put: expected key length 40, actual %d" % keyLen
        elif self.usingSHA == Q.USING_SHA2 and keyLen != SHA2_HEX_LEN:
            errMsg = "UDir.put: expected key length 64, actual %d" % keyLen
        elif self.usingSHA == Q.USING_SHA3 and keyLen != SHA3_HEX_LEN:
            errMsg = "UDir.put: expected key length 64, actual %d" % keyLen
        # XXX BAD USING OR LEN NOT ALLOWED FOR
        if errMsg:
            raise XLUError(errMsg)

        if self.usingSHA == Q.USING_SHA1:
            hash = fileSHA1Hex(inFile)
        elif self.usingSHA == Q.USING_SHA2:
            hash = fileSHA2Hex(inFile)
        elif self.usingSHA == Q.USING_SHA3:
            hash = fileSHA3Hex(inFile)
        # XXX BAD USING OR LEN NOT ALLOWED FOR
        length = os.stat(inFile).st_size

        if self.dirStruc == UDir.DIR_FLAT:
            fullishPath = os.path.join(self.uPath, key)
        else:
            if self.dirStruc == UDir.DIR16x16:
                topSubDir = hash[0]
                lowerDir = hash[1]
            elif self.dirStruc == UDir.DIR256x256:
                topSubDir = hash[0:2]
                lowerDir = hash[2:4]
            else:
                raise XLUError("unknown dirStruc %d" % self.dirStruc)
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
        if self.usingSHA == Q.USING_SHA1:
            # FIX ME FIX ME FIX ME
            sha = hashlib.sha1()
        else:
            sha = hashlib.sha256()
        sha.update(data)
        hash = sha.hexdigest()
        length = len(data)

        if self.dirStruc == UDir.DIR_FLAT:
            fullishPath = os.path.join(self.uPath, key)
        else:
            if self.dirStruc == UDir.DIR16x16:
                topSubDir = hash[0]
                lowerDir = hash[1]
            elif self.dirStruc == UDir.DIR256x256:
                topSubDir = hash[0:2]
                lowerDir = hash[2:4]
            else:
                raise XLUError("undefined dirStruc %d" % self.dirStruc)

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

        # XXX UNSATISFACTORY HANDLING OF THE ERROR
        if (hash != key):
            errMsg = "putData:\n\texpected key %s\n\tcontent hash %s" % (
                key, hash)
            print(errMsg)

        return (length, hash)               # GEEP2

    def exists(self, key):
        """ key is hexadecimal content key """

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
        if self.dirStruc == UDir.DIR_FLAT:
            return os.path.join(self.uPath, key)

        if self.dirStruc == UDir.DIR16x16:
            topSubDir = key[0]
            lowerDir = key[1]
        elif self.dirStruc == UDir.DIR256x256:
            topSubDir = key[0:2]
            lowerDir = key[2:4]
        else:
            raise XLUError("unexpected dirStruc %d" % self.dirStruc)

        return self.uPath + '/' + topSubDir + '/' + lowerDir + '/' + key

    def reStruc(self, newStruc):
        """
        Change the structure of uDir to the new dirStruc specified,
        where newStruc is a small non-negative integer.
        """
        oldStruc = self.dirStruc
        oldSig = UDir.dirStrucSig(self.uPath, self.dirStruc, self.usingSHA)
        newSig = UDir.dirStrucSig(self.uPath, newStruc, self.usingSHA)

        # fix signature
        if newSig != oldSig:
            if os.path.exists(oldSig):
                os.unlink(oldSig)
            if not os.path.exists(newSig):
                sigBase = os.path.dirname(newSig)
                os.makedirs(sigBase, exist_ok=True)
                open(newSig, 'a').close()                # touch
        self._dirStruc = newStruc

        self._simpleRestruc(oldStruc, newStruc)

    def _simpleRestruc(self, oldStruc, newStruc):
        """
        Scan the directory structure looking for files whose name=content hash
        of the right length for the SHA used (so 40 bytes for SHA1, 64 for SHA2/3)
        but in the wrong directory.  Out-of-place files are moved to the correct
        directory.
        """

        pathToTop = self.uPath
        # DEBUG
        # print("pathToTop: %s" % pathToTop)
        # END
        if oldStruc == UDir.DIR_FLAT:
            for key in os.listdir(pathToTop):
                if self.usingSHA == Q.USING_SHA1:
                    # FIX ME FIX ME FIX ME
                    m = self.HEX_FILE_NAME_1_RE.match(key)
                else:
                    m = self.HEX_FILE_NAME_2_RE.match(key)
                if m:
                    # DEBUG
                    # print("match: %s" % key)
                    # END
                    pathToFile = os.path.join(pathToTop, key)
                    self.put(pathToFile, key)

        else:
            # oldStruc == UDir.DIR16x16 or UDir.DIR256x256
            if oldStruc == UDir.DIR16x16:
                dirRE = self.HEX_DIR_NAME_16_RE
            else:
                dirRE = self.HEX_DIR_NAME_256_RE
            for midDir in os.listdir(pathToTop):
                midOccupied = False
                m = dirRE.match(midDir)
                if m:
                    pathToMid = os.path.join(pathToTop, midDir)
                    # DEBUG
                    # print("pathToMid: %s" % pathToMid)
                    # END
                    for botDir in os.listdir(pathToMid):
                        botOccupied = False
                        m = dirRE.match(botDir)
                        if m:
                            pathToBot = os.path.join(pathToMid, botDir)
                            # DEBUG
                            # print("pathToBot: %s" % pathToBot)
                            # END
                            for key in os.listdir(pathToBot):
                                if self.usingSHA == Q.USING_SHA1:
                                    # FIX ME FIX ME FIX ME
                                    m = self.HEX_FILE_NAME_1_RE.match(key)
                                else:
                                    m = self.HEX_FILE_NAME_2_RE.match(key)
                                if m:
                                    # DEBUG
                                    # print("match at bottom: %s" % key)
                                    # END
                                    pathToFile = os.path.join(pathToBot, key)
                                    self.put(pathToFile, key)
                                else:
                                    botOccupied = True
                        if not botOccupied:
                            os.rmdir(pathToBot)
                    if not midOccupied:
                        os.rmdir(pathToMid)

        # remove old directories
