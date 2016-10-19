#!/usr/bin/python3

# ~/dev/py/xlattice_py/xlattice/stats.py

import os
import re
import shutil
import stat
import sys
from argparse import ArgumentParser

from xlattice import (__version__, __version_date__, Q)
from xlattice.u import (file_sha1hex, UDir,)

###############################
# XXX assumes usingSHA == True
###############################

HEX2_PAT = '^[0-9a-fA-F][0-9a-fA-F]$'
HEX2_RE = re.compile(HEX2_PAT)

SHA1_PAT = '^[0-9a-fA-F]{40}$'
SHA1_RE = re.compile(SHA1_PAT)


class UStats:

    def __init__(self):
        self._dirStruc = UDir.DIR_FLAT
        self._usingSHA = False

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
    def dir_struc(self): return self._dirStruc   # an int

    @property
    def using_sha(self): return self._usingSHA

    @property
    def subdir_count(self):
        return self._subDirCount

    @property
    def sub_subdir_count(self):
        return self._subSubDirCount

    @property
    def leaf_count(self):
        return self._leafCount

    @property
    def odd_count(self):
        return self._oddCount

    @property
    def has_l(self):
        return self._hasL

    @property
    def has_node_id(self):
        return self._hasNodeID

    @property
    def min_leaf_bytes(self):
        return self._minLeafBytes

    @property
    def max_leaf_bytes(self):
        return self._maxLeafBytes

    @property
    def unexpected_at_top(self):
        return self._unexpectedAtTop


def scan_leaf_dir(pathToDir, obj):
    # DEBUG
    # #print("    scanning leaf directory %s" % pathToDir)
    # END
    file_count = 0
    odd_count = 0
    for file in os.listdir(pathToDir):
        # DEBUG
        # print("      leaf file: %s" % file)
        # END
        m = SHA1_RE.match(file)
        if m:
            file_count = file_count + 1
            pathToFile = os.path.join(pathToDir, file)
            size = os.stat(pathToFile).st_size
            if size < obj.min_leaf_bytes:
                obj._minLeafBytes = size
            if size > obj.max_leaf_bytes:
                obj._maxLeafBytes = size
        else:
            odd_count = odd_count + 1
    obj._leafCount += file_count
    obj._oddCount += odd_count


def collect_stats(u_path, out_path, verbose):

    string = UStats()        # we will return this

    # XXX outPath IS NOT USED
    if out_path:
        os.makedirs(out_path, exist_ok=True)
    # END NOT USED

    u_dir = UDir.discover(u_path)
    string._usingSHA = u_dir.using_sha
    string._dirStruc = u_dir.dir_struc

    # upper-level files / subdirectories
    top_files = os.listdir(u_path)
    for top_file in top_files:

        # -- upper-level files ----------------------------------------

        # At this level we expect 00-ff, tmp/ and in/ subdirectories
        # plus the files L and possibly nodeID.

        m = HEX2_RE.match(top_file)
        if m:

            # -- upper-level directories ------------------------------

            string._subDirCount += 1
            pathToSubDir = os.path.join(u_path, top_file)
            # DEBUG
            #print("SUBDIR: %s" % pathToSubDir)
            # END
            mid_files = os.listdir(pathToSubDir)
            for mid_file in mid_files:
                m2 = HEX2_RE.match(mid_file)
                if m2:
                    string._subSubDirCount += 1
                    pathToSubSubDir = os.path.join(pathToSubDir, mid_file)
                    # DEBUG
                    #print("  SUBSUBDIR: %s" % pathToSubSubDir)
                    # END
                    for subSubFile in os.listdir(pathToSubSubDir):
                        scan_leaf_dir(pathToSubSubDir, string)

                # -- other upper-level files --------------------------
                else:
                    path_to_oddity = os.path.join(pathToSubDir, mid_file)
                    # print("unexpected: %s" % pathToOddity)
                    string._oddCount += 1

        #-- other upper-level files -----------------------------------

        else:
            if top_file == 'L':
                string._hasL = True
            elif top_file == 'node_id':
                string._hasNodeID = True
            elif top_file in ['in', 'tmp']:
                # DEBUG
                # print("TOP LEVEL OTHER DIR: %s" % topFile)
                pathToDir = os.path.join(u_path, top_file)
                scan_leaf_dir(pathToDir, string)
            else:
                path_to_oddity = os.path.join(u_path, top_file)
                string._unexpectedAtTop.append(path_to_oddity)
                string._oddCount += 1

    return string
