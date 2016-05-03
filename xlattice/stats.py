#!/usr/bin/python3

# ~/dev/py/xlattice_py/stats

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

HEX2_PAT = '^[0-9a-f][0-9a-f]$'
HEX2_RE = re.compile(HEX2_PAT)

SHA1_PAT = '^[0-9a-f]{40}$'
SHA1_RE = re.compile(SHA1_PAT)


def scanLeafDir(pathToDir):
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
        else:
            occCount = oddCount + 1
    return fileCount, oddCount


def collectStats(uDir, outDir, verbose):

    leafCount = 0
    subDirCount = 0
    subSubDirCount = 0
    oddCount = 0
    hasL = False
    hasNodeID = False

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

            subDirCount = subDirCount + 1
            pathToSubDir = os.path.join(uDir, topFile)
            # DEBUG
            #print("SUBDIR: %s" % pathToSubDir)
            # END
            midFiles = os.listdir(pathToSubDir)
            for midFile in midFiles:
                m2 = HEX2_RE.match(midFile)
                if m2:
                    subSubDirCount = subSubDirCount + 1
                    pathToSubSubDir = os.path.join(pathToSubDir, midFile)
                    # DEBUG
                    #print("  SUBSUBDIR: %s" % pathToSubSubDir)
                    # END
                    for subSubFile in os.listdir(pathToSubSubDir):
                        n, odd = scanLeafDir(pathToSubSubDir)
                        leafCount = leafCount + n
                        oddCount = oddCount + odd

                # -- other upper-level files --------------------------
                else:
                    pathToOddity = os.path.join(pathToSubDir, midFile)
                    # print("unexpected: %s" % pathToOddity)
                    oddCount = oddCount + 1

        #-- other upper-level files -----------------------------------

        else:
            if topFile == 'L':
                hasL = True
            elif topFile == 'nodeID':
                hasNodeID = True
            elif topFile in ['in', 'tmp']:
                # DEBUG
                # print("TOP LEVEL OTHER DIR: %s" % topFile)
                pathToDir = os.path.join(uDir, topFile)
                n, odd = scanLeafDir(pathToDir)
                leafCount = leafCount + n
                oddCount = oddCount + odd
            else:
                pathToOddity = os.path.join(uDir, topFile)
                # print("unexpected: %s" % pathToOddity)
                oddCount = oddCount + 1

    return subDirCount, subSubDirCount, leafCount, oddCount, hasL, hasNodeID
