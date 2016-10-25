#!/usr/bin/python3

# ~/dev/py/xlattice_py/xlattice/stats.py

import os
import re
import shutil
import stat
import sys
from argparse import ArgumentParser

from xlattice import (__version__, __version_date__, QQQ)
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
        self._using_sha = False

        self._sub_dir_count = 0
        self._subSubDirCount = 0
        self._leaf_count = 0
        self._oddCount = 0
        self._has_l = False
        self._hasNodeID = False
        self._minLeafBytes = sys.maxsize
        self._max_leaf_bytes = 0

        self._unexpectedAtTop = []

    @property
    def dir_struc(self): return self._dirStruc   # an int

    @property
    def using_sha(self): return self._using_sha

    @property
    def subdir_count(self):
        return self._sub_dir_count

    @property
    def sub_subdir_count(self):
        return self._subSubDirCount

    @property
    def leaf_count(self):
        return self._leaf_count

    @property
    def odd_count(self):
        return self._oddCount

    @property
    def has_l(self):
        return self._has_l

    @property
    def has_node_id(self):
        return self._hasNodeID

    @property
    def min_leaf_bytes(self):
        return self._minLeafBytes

    @property
    def max_leaf_bytes(self):
        return self._max_leaf_bytes

    @property
    def unexpected_at_top(self):
        return self._unexpectedAtTop


def scan_leaf_dir(path_to_dir, obj):
    # DEBUG
    # #print("    scanning leaf directory %s" % pathToDir)
    # END
    file_count = 0
    odd_count = 0
    for file in os.listdir(path_to_dir):
        # DEBUG
        # print("      leaf file: %s" % file)
        # END
        match = SHA1_RE.match(file)
        if match:
            file_count = file_count + 1
            path_to_file = os.path.join(path_to_dir, file)
            size = os.stat(path_to_file).st_size
            if size < obj.min_leaf_bytes:
                obj._minLeafBytes = size
            if size > obj.max_leaf_bytes:
                obj._max_leaf_bytes = size
        else:
            odd_count = odd_count + 1
    obj._leaf_count += file_count
    obj._oddCount += odd_count


def collect_stats(u_path, out_path, verbose):

    string = UStats()        # we will return this

    # XXX outPath IS NOT USED
    if out_path:
        os.makedirs(out_path, exist_ok=True)
    # END NOT USED

    u_dir = UDir.discover(u_path)
    string._using_sha = u_dir.using_sha
    string._dirStruc = u_dir.dir_struc

    # upper-level files / subdirectories
    top_files = os.listdir(u_path)
    for top_file in top_files:

        # -- upper-level files ----------------------------------------

        # At this level we expect 00-ff, tmp/ and in/ subdirectories
        # plus the files L and possibly nodeID.

        match = HEX2_RE.match(top_file)
        if match:

            # -- upper-level directories ------------------------------

            string._sub_dir_count += 1
            path_to_sub_dir = os.path.join(u_path, top_file)
            # DEBUG
            #print("SUBDIR: %s" % pathToSubDir)
            # END
            mid_files = os.listdir(path_to_sub_dir)
            for mid_file in mid_files:
                match2 = HEX2_RE.match(mid_file)
                if match2:
                    string._subSubDirCount += 1
                    pathToSubSubDir = os.path.join(path_to_sub_dir, mid_file)
                    # DEBUG
                    #print("  SUBSUBDIR: %s" % pathToSubSubDir)
                    # END
                    for sub_sub_file in os.listdir(pathToSubSubDir):
                        scan_leaf_dir(pathToSubSubDir, string)

                # -- other upper-level files --------------------------
                else:
                    path_to_oddity = os.path.join(path_to_sub_dir, mid_file)
                    # print("unexpected: %s" % pathToOddity)
                    string._oddCount += 1

        #-- other upper-level files -----------------------------------

        else:
            if top_file == 'L':
                string._has_l = True
            elif top_file == 'node_id':
                string._hasNodeID = True
            elif top_file in ['in', 'tmp']:
                # DEBUG
                # print("TOP LEVEL OTHER DIR: %s" % topFile)
                path_to_dir = os.path.join(u_path, top_file)
                scan_leaf_dir(path_to_dir, string)
            else:
                path_to_oddity = os.path.join(u_path, top_file)
                string._unexpectedAtTop.append(path_to_oddity)
                string._oddCount += 1

    return string
