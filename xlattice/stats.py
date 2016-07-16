#!/usr/bin/python3

# ~/dev/py/xlattice_py/xlattice/stats.py

import os
import re
import shutil
import stat
import sys
from argparse import ArgumentParser

from xlattice import (__version__, __version_date__)
from xlattice.u import fileSHA1Hex

###############################
# XXX assumes usingSHA1 == True
###############################

HEX2_PAT = '^[0-9a-fA-F][0-9a-fA-F]$'
HEX2_RE = re.compile(HEX2_PAT)

SHA1_PAT = '^[0-9a-fA-F]{40}$'
SHA1_RE = re.compile(SHA1_PAT)


class UStats:

    def __init__(self):
        self._subDirCount = 0
        self._subSubDirCount = 0
        self._leafCount = 0
        self._oddCount = 0
        self._hasL = False
        self._hasNodeID = False
        self._minLeafBytes = sys.maxsize
        self._maxLeafBytes = 0

    @property
    def subDirCount(self):
        return self._subDirCount

    @subDirCount.setter
    def subDirCount(self, value):
        self._subDirCount = value

    @property
    def subSubDirCount(self):
        return self._subSubDirCount

    @subSubDirCount.setter
    def subSubDirCount(self, value):
        self._subSubDirCount = value

    @property
    def leafCount(self):
        return self._leafCount

    @leafCount.setter
    def leafCount(self, value):
        self._leafCount = value

    @property
    def oddCount(self):
        return self._oddCount

    @oddCount.setter
    def oddCount(self, value):
        self._oddCount = value

    @property
    def hasL(self):
        return self._hasL

    @hasL.setter
    def hasL(self, value):
        self._hasL = value

    @property
    def hasNodeID(self):
        return self._hasNodeID

    @hasNodeID.setter
    def hasNodeID(self, value):
        self._hasNodeID = value

    @property
    def minLeafBytes(self):
        return self._minLeafBytes

    @minLeafBytes.setter
    def minLeafBytes(self, value):
        """ Try to set the value, succeeding if its smaller """
        if value < self.minLeafBytes:
            self._minLeafBytes = value

    @property
    def maxLeafBytes(self):
        return self._maxLeafBytes

    @maxLeafBytes.setter
    def maxLeafBytes(self, value):
        """ Try to set the value, succeeding if its larger """
        if value > self.maxLeafBytes:
            self._maxLeafBytes = value


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
            obj.minLeafBytes = size
            obj.maxLeafBytes = size
        else:
            oddCount = oddCount + 1
    obj.leafCount += fileCount
    obj.oddCount += oddCount


def collectStats(uDir, outDir, verbose):

    s = UStats()        # we will return this

    if outDir:
        os.makedirs(outDir, exist_ok=True)

    # upper-level files / subdirectories
    topFiles = os.listdir(uDir)
    for topFile in topFiles:

        # -- upper-level files ----------------------------------------

        # At this level we expect 00-ff, tmp/ and in/ subdirectories
        # plus the files L and possibly nodeID.

        m = HEX2_RE.match(topFile)
        if m:

            # -- upper-level directories ------------------------------

            s.subDirCount += 1
            pathToSubDir = os.path.join(uDir, topFile)
            # DEBUG
            #print("SUBDIR: %s" % pathToSubDir)
            # END
            midFiles = os.listdir(pathToSubDir)
            for midFile in midFiles:
                m2 = HEX2_RE.match(midFile)
                if m2:
                    s.subSubDirCount += 1
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
                    oddCount += 1

        #-- other upper-level files -----------------------------------

        else:
            if topFile == 'L':
                s.hasL = True
            elif topFile == 'nodeID':
                s.hasNodeID = True
            elif topFile in ['in', 'tmp']:
                # DEBUG
                # print("TOP LEVEL OTHER DIR: %s" % topFile)
                pathToDir = os.path.join(uDir, topFile)
                scanLeafDir(pathToDir, s)
            else:
                pathToOddity = os.path.join(uDir, topFile)
                # DEBUB
                print("unexpected at top level: %s" % pathToOddity)
                # END
                s.oddCount += 1

    return s
