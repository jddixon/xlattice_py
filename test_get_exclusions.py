#!/usr/bin/env python3
# testGetExclusions.py

""" Test the glob/wildcard functions in xlattice/util.py """

import hashlib
import os
import re
import shutil
import time
import unittest

from xlattice.util import getExclusions, makeExRE
from rnglib import SimpleRNG


class TestGetExclusions(unittest.TestCase):
    """ Test the glob/wildcard functions in xlattice/util.py """

    def setUp(self):
        self.rng = SimpleRNG(time.time())                 # XXX NOT USED

    def tearDown(self):
        pass

    def doTestForExpectedExclusions(self, exRE):
        # should always match
        self.assertIsNotNone(exRE.match('merkle.pyc'))
        self.assertIsNotNone(exRE.match('.svn'))
        self.assertIsNotNone(exRE.match('.foo.swp'))          # vi backup file
        self.assertIsNotNone(exRE.match('junkEverywhere')
                             )    # begins with 'junk'
        self.assertIsNotNone(exRE.match('.merkle'))

    def doTestForExpectedMatches(self, matchRE, names):
        for name in names:
            self.assertIsNotNone(matchRE.match(name))

    def doTestForExpectedMatchFailures(self, matchRE, names):
        for name in names:
            m = matchRE.match(name)
            if m:
                print("WE HAVE A MATCH ON '%s'" % name)
            # self.assertEquals( None, where )

    def doTestGetExclusions(self, projDir):
        """
        This test assumes that there is a local .gitignore containing
        at least '.merkle', '.svn*' '*.swp', and 'junk*'
        """

        # convert .gitignore's contents to a list of parenthesized
        # regular expressions
        globs = getExclusions(projDir, '.gitignore')
        self.assertIsNotNone(len(globs) > 0)

        exRE = makeExRE(globs)
        self.assertIsNotNone(exRE is not None)
        self.doTestForExpectedExclusions(exRE)

    def testGetExclusions(self):
        self.doTestGetExclusions('.')

if __name__ == '__main__':
    unittest.main()
