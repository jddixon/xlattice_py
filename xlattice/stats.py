#!/usr/bin/python3

# ~/dev/py/xlattice_py/xlattice/stats.py

import os
import re
import shutil
import stat
import sys
from argparse import ArgumentParser

from xlattice import (__version__, __version_date__)
from xlattice.u import (fileSHA1Hex, UDir,)

###############################
# XXX assumes usingSHA1 == True
###############################

HEX2_PAT = '^[0-9a-fA-F][0-9a-fA-F]$'
HEX2_RE = re.compile(HEX2_PAT)

SHA1_PAT = '^[0-9a-fA-F]{40}$'
SHA1_RE = re.compile(SHA1_PAT)


class UStats:

    def __init__(self):
        self._dirStruc = UDir.DIR_FLAT
        self._usingSHA1 = False

        self._subDirCount = 0
        self._subSubDirCount = 0
        self._leafCount = 0
        self._oddCount = 0
        self._hasL = False
        self._hasNodeID = False
        self._minLeafBytes = sys.maxsize
        self._maxLeafBytes = 0

        self._unexpectedAtTop = []

    @property
    def dirStruc(self): return self._dirStruc   # an int

    @property
    def usingSHA1(self): return self._usingSHA1

    @property
    def subDirCount(self):
        return self._subDirCount

    @property
    def subSubDirCount(self):
        return self._subSubDirCount

    @property
    def leafCount(self):
        return self._leafCount

    @property
    def oddCount(self):
        return self._oddCount

    @property
    def hasL(self):
        return self._hasL

    @property
    def hasNodeID(self):
        return self._hasNodeID

    @property
    def minLeafBytes(self):
        return self._minLeafBytes

    @property
    def maxLeafBytes(self):
        return self._maxLeafBytes

    @property
    def unexpectedAtTop(self):
        return self._unexpectedAtTop


def scanLeafDir(pathToDir, obj):
    # DEBUG
    # #print("    scanning leaf directory %s" % pathToDir)
    # END
    fileCount = 0
    oddCount = 0
    for file in os.listdir(pathToDir):
        # DEBUG
        # print("      leaf file: %s" % file)
        # END
        m = SHA1_RE.match(file)
        if m:
            fileCount = fileCount + 1
            pathToFile = os.path.join(pathToDir, file)
            size = os.stat(pathToFile).st_size
            if size < obj.minLeafBytes:
                obj._minLeafBytes = size
            if size > obj.maxLeafBytes:
                obj._maxLeafBytes = size
        else:
            oddCount = oddCount + 1
    obj._leafCount += fileCount
    obj._oddCount += oddCount


def collectStats(uPath, outPath, verbose):

    s = UStats()        # we will return this

    # XXX outPath IS NOT USED
    if outPath:
        os.makedirs(outPath, exist_ok=True)
    # END NOT USED

    uDir = UDir.discover(uPath)
    s._usingSHA1 = uDir.usingSHA1
    s._dirStruc = uDir.dirStruc

    # upper-level files / subdirectories
    topFiles = os.listdir(uPath)
    for topFile in topFiles:

        # -- upper-level files ----------------------------------------

        # At this level we expect 00-ff, tmp/ and in/ subdirectories
        # plus the files L and possibly nodeID.

        m = HEX2_RE.match(topFile)
        if m:

            # -- upper-level directories ------------------------------

            s._subDirCount += 1
            pathToSubDir = os.path.join(uPath, topFile)
            # DEBUG
            #print("SUBDIR: %s" % pathToSubDir)
            # END
            midFiles = os.listdir(pathToSubDir)
            for midFile in midFiles:
                m2 = HEX2_RE.match(midFile)
                if m2:
                    s._subSubDirCount += 1
                    pathToSubSubDir = os.path.join(pathToSubDir, midFile)
                    # DEBUG
                    #print("  SUBSUBDIR: %s" % pathToSubSubDir)
                    # END
                    for subSubFile in os.listdir(pathToSubSubDir):
                        scanLeafDir(pathToSubSubDir, s)

                # -- other upper-level files --------------------------
                else:
                    pathToOddity = os.path.join(pathToSubDir, midFile)
                    # print("unexpected: %s" % pathToOddity)
                    s._oddCount += 1

        #-- other upper-level files -----------------------------------

        else:
            if topFile == 'L':
                s._hasL = True
            elif topFile == 'nodeID':
                s._hasNodeID = True
            elif topFile in ['in', 'tmp']:
                # DEBUG
                # print("TOP LEVEL OTHER DIR: %s" % topFile)
                pathToDir = os.path.join(uPath, topFile)
                scanLeafDir(pathToDir, s)
            else:
                pathToOddity = os.path.join(uPath, topFile)
                s._unexpectedAtTop.append(pathToOddity)
                s._oddCount += 1

    return s
