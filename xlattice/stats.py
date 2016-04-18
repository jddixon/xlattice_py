#!/usr/bin/python3

# ~/dev/py/xlattice_py/stats

import os, re, shutil, stat, sys
from argparse import ArgumentParser

from xlattice import (__version__, __version_date__)
from xlattice.u import fileSHA1Hex

###############################
# XXX assumes usingSHA1 == True
###############################

HEX2_PAT = '^[0-9a-f][0-9a-f]$'
HEX2_RE  = re.compile(HEX2_PAT)

def scanLeafDir(pathToDir):
    fileCount = 0
    oddCount  = 0
    for file in os.listdir(pathToDir):
        m = HEX2_RE.match(file)
        if m:
            fileCount = fileCount + 1
        else:
            occCount  = oddCount + 1
    return fileCount, oddCount

def collectStats(inDir, outDir, verbose):

    leafCount = 0
    subDirCount = 0
    subSubDirCount = 0
    oddCount       = 0
    hasL            = False
    hasNodeID       = False

    if outDir:
        os.makedirs(outDir, exist_ok=True)

    # top level files / subdirectories
    topFiles = os.listdir(inDir)
    for topFile in topFiles:
       
        # -- top level files ----------------------------------------

        # At this level we expect 00-ff, tmp/ and in/ subdirectories 
        # plus the files L and possibly nodeID.
        
        m = HEX2_RE.match(topFile)
        if m: 

            # -- mid-level directories ------------------------------

            subDirCount = subDirCount + 1
            pathToSubDir = os.path.join(inDir, topFile)

            midFiles = os.listdir(pathToSubDir)
            for midFile in midFiles:
                m2 = HEX2_RE.match(midFile)
                if m2:
                    pathToSubSubDir = os.path.join(pathToSubDir, midFile)
                    for subSubFile in os.listdir(pathToSubSubDir):
                        subSubDirCount = subSubDirCount + 1
                        n, odd = scanLeafDir(pathToSubSubDir)
                        leafCount = leafCount + n
                        oddCount  = oddCount + odd
                        
                # -- other mid-level files --------------------------
                else:
                    pathToOddity = os.path.join(pathToSubDir, midFile)
                    print("unexpected: %s" % pathToOddity)
                    oddCount = oddCount + 1

        #-- other top level files -----------------------------------

        else:
            if topFile == 'L':
                hasL = True
            elif topFile == 'nodeID':
                hasNodeID = True
            elif topFile == 'in' or topFile == 'tmp':
                pathToDir = os.path.join(inDir, topFile)
                n, odd = scanLeafDir(pathToDir)
                leafCount = leafCount + n
                oddCount  = oddCount  + odd
            else:
                pathToOddity = os.path.join(inDir, topFile)
                print("unexpected: %s" % pathToOddity)
                oddCount = oddCount + 1
    
    return subDirCount, subSubDirCount, leafCount, oddCount, hasL, hasNodeID
