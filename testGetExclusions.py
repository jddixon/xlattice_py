#!/usr/bin/python3

# testGetExclusions.py

import hashlib
import os
import re
import shutil
import time
import unittest

from merkletree import MerkleDoc                        # FOR TESTING ??

from xlattice.util import getExclusions
from rnglib import SimpleRNG


class TestGetExclusions (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())                 # XXX NOT USED

    def tearDown(self):
        pass

    def doTestForExpectedExclusions(self, exRE):
        # should always match
        self.assertTrue(exRE.search('merkle.pyc'))
        self.assertTrue(exRE.search('.svn'))
        self.assertTrue(exRE.search('.foo.swp'))          # vi backup file
        self.assertTrue(exRE.search('junkEverywhere'))    # begins with 'junk'

    def doTestForExpectedMatches(self, matchRE, names):
        for name in names:
            self.assertTrue(matchRE.search(name))

    def doTestForExpectedMatchFailures(self, matchRE, names):
        for name in names:
            m = matchRE.search(name)
            if m:
                print("WE HAVE A MATCH ON '%s'" % name)
            # self.assertEquals( None, where )

    def doTestGetExclusions(self, projDir):
        """
        This test assumes that there is a local .gitignore containing
        at least '.merkle', '.svn*' '*.swp', and 'junk*'
        """
        exclPat = getExclusions(projDir, '.gitignore')
        exRE = re.compile(exclPat)
        self.assertTrue(exRE is not None)
        self.doTestForExpectedExclusions(exRE)

    def testGetExclusions(self):
        self.doTestGetExclusions('.')

if __name__ == '__main__':
    unittest.main()
