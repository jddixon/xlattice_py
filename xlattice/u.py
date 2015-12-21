# xlattice_py/xlattice/u.py

__all__ = [ 
            'fileSHA1', 'fileSHA2',         # DEPRECATED
            'fileSHA1Bin', 'fileSHA2Bin', 'fileSHA1Hex', 'fileSHA2Hex',
            'copyAndPut1',  'getData1', 'put1',         'putData1',
            'copyAndPut2',  'getData2', 'put2',         'putData2',
            # should be same code for u1 and u2
            'exists',       'fileLen',      'getPathForKey',

            # classes -------------------------------------
            'ULock',                # used??
        ]

import io, os, shutil, time
import hashlib, sys
import rnglib # for rnglib.nextFileName

# CONSTANTS ========================================================-

RNG = rnglib.SimpleRNG(time.time())

# - fileSHA1 --------------------------------------------------------
# returns the SHA1 hash of the contents of a file

# DEPRECATED
def fileSHA1 (path):
    return fileSHA1Hex(path)
# END DEPRECATED

def fileSHA1Bin(path):
    if path == None or not os.path.exists(path):
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
    if path == None or not os.path.exists(path):
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

# - fileSHA2 --------------------------------------------------------
# returns the SHA256 hash of the contents of a file

# DEPRECATED
def fileSHA2 (path):
    return fileSHA2Hex(path)
# END DEPRECATED


def fileSHA2Bin(path):
    if path == None or not os.path.exists(path):
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
    if path == None or not os.path.exists(path):
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

# SHA1-BASED u256x256 METHODS =======================================

#- copyAndPut1 -------------------------------------------------------
def copyAndPut1(path, uPath, key):
    # the temporary file MUST be created on the same device 
    tmpDir = os.path.join(uPath, 'tmp')
    # xxx POSSIBLE RACE CONDITION
    tmpFileName = os.path.join(tmpDir, RNG.nextFileName(16))
    while os.path.exists(tmpFileName):
        tmpFileName = os.path.join(tmpDir, RNG.nextFileName(16))
    shutil.copyfile(path, tmpFileName)
    return put1(tmpFileName, uPath, key)

# - getData1 ---------------------------------------------------------
def getData1(uPath, key):
    path = getPathForKey(uPath, key)
    if not os.path.exists(path):
        return None
    else:
        with open(path,'rb') as f:
            data = f.read()
        return data

# - put1 -------------------------------------------------------------
# tmp is the path to a local file which will be renamed into U (or deleted
# if it is already present in U)
# uPath is an absolute or relative path to a U directory organized 256x256
# key is an sha1 content hash.
# If the operation succeeds we return the length of the file (which must
# not be zero.  Otherwise we return 0.
# we don't do much checking
def put1(inFile, uPath, key):
    hash = fileSHA1(inFile)
    if (hash != key):
        print("expected %s to have key %s, but the content key is %s" % (
                inFile, key, hash))
        return (0, None)
    len = os.stat(inFile).st_size
    topSubDir = hash[0:2]
    lowerDir  = hash[2:4]
    targetDir = uPath + '/' + topSubDir + '/' + lowerDir + '/'
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)
    fullishPath = targetDir + key
    if (os.path.exists(fullishPath)):
        os.unlink(inFile)
    else:
        os.rename(inFile, fullishPath)
        os.chmod(fullishPath, 0o444)
    return (len, hash) #

# - putData1 ---------------------------------------------------------
def putData1(data, uPath, key):
    s = hashlib.sha1()
    s.update(data)
    hash = s.hexdigest()
    if (hash != key):
        print("expected data to have key %s, but the content key is %s" % (
               key, hash))
        return (0, None)        # length and hash
    length = len(data)          # XXX POINTLESS
    topSubDir = hash[0:2]
    lowerDir  = hash[2:4]
    targetDir = uPath + '/' + topSubDir + '/' + lowerDir + '/'
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

# SHA256-BASED u256x256 METHODS =====================================

#- copyAndPut2 ------------------------------------------------------
def copyAndPut2(path, uPath, key):
    # the temporary file MUST be created on the same device
    tmpDir = os.path.join(uPath, 'tmp')
    # xxx POSSIBLE RACE CONDITION
    tmpFileName = os.path.join(tmpDir, RNG.nextFileName(16))
    while os.path.exists(tmpFileName):
        tmpFileName = os.path.join(tmpDir, RNG.nextFileName(16))
    shutil.copyfile(path, tmpFileName)
    return put2(tmpFileName, uPath, key)

# - getData2 --------------------------------------------------------
def getData2(uPath, key):
    path = getPathForKey(uPath, key)
    if not os.path.exists(path):
        return None
    else:
        with open(path,'rb') as f:
            data = f.read()
        return data

# - put2 ------------------------------------------------------------
# tmp is the path to a local file which will be renamed into U (or deleted
# if it is already present in U)
# uPath is an absolute or relative path to a U directory organized 256x256
# key is an sha3 content hash.
# If the operation succeeds we return the length of the file (which must
# not be zero.  Otherwise we return 0.
# we don't do much checking
def put2(inFile, uPath, key):
    hash = fileSHA2(inFile)
    if (hash != key):
        print("expected %s to have key %s, but the content key is %s" % (
                inFile, key, hash))
        return (0, None)
    len = os.stat(inFile).st_size
    topSubDir = hash[0:2]
    lowerDir  = hash[2:4]
    targetDir = uPath + '/' + topSubDir + '/' + lowerDir + '/'
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)
    fullishPath = targetDir + key
    if (os.path.exists(fullishPath)):
        os.unlink(inFile)
    else:
        os.rename(inFile, fullishPath)
        os.chmod(fullishPath, 0o444)
    return (len, hash) #

# - putData2 --------------------------------------------------------
def putData2(data, uPath, key):
    s = hashlib.sha256()
    s.update(data)
    hash = s.hexdigest()
    if (hash != key):
        print("expected data to have key %s, but the content key is %s" % (
               key, hash))
        return (0, None)        # length and hash
    length = len(data)          # XXX POINTLESS
    topSubDir = hash[0:2]
    lowerDir  = hash[2:4]
    targetDir = uPath + '/' + topSubDir + '/' + lowerDir + '/'
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


# COMMON FUNCTIONS ==================================================

# XXX DEPRECATED ####################################################
def getPath(uPath, key):
    path = getPathForKey(uPath, key)
    if (os.path.exists(path)):
        return path
    else:
        print("HASH %s: FULLISH PATH DOES NOT EXIST: %s" % (key, path))
        return None
# END DEPRECATED ####################################################

# - exists ----------------------------------------------------------
def exists(uPath, key):
    path = getPathForKey(uPath, key)
    return os.path.exists(path)

# - fileLen ---------------------------------------------------------
# returns the length of the file with the given content key
def fileLen(uPath, key):
    path = getPathForKey(uPath, key)
    return os.stat(path).st_size

# - getPathForKey ---------------------------------------------------
# returns a path to a file with the content key passed, or None if there
# is no such file
def getPathForKey(uPath, key):
    if(os.path.exists(uPath) == False):
        print("HASH %s: UDIR DOES NOT EXIST: %s" % (key, uPath))
        return None
    topSubDir = key[0:2]
    lowerDir  = key[2:4]
    return uPath + '/' + topSubDir + '/' + lowerDir + '/' + key

# ulock CLASSES =====================================================

class ULock:
    # these are UNPROTECTED
    __slots__ = ['lockDir', 'lockFile', 'pid']

    def __init__(self, uDir = '/var/U'):
        self.pid = os.getpid()
        absPathToU    = os.path.abspath(uDir)
        self.lockDir  = '/tmp/u' + absPathToU
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
