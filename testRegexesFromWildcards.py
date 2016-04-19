#!/usr/bin/python3

# testRegexesFromWildcards.py

import hashlib
import os
import re
import shutil
import time
import unittest
from rnglib import SimpleRNG
from xlattice.util import regexesFromWildcards


class TestRegexesFromWildcards (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    # utility functions #############################################
    def makeExRE(self, globs):
        """
        Given a list of globs aka wildcards, return a compiled regular
        expression representing a match on one or more globs.
        """
        r = regexesFromWildcards(globs)
        return re.compile('|'.join(r))

    def doTestForExpectedMatches(self, matchRE, names):
        for name in names:
            self.assertIsNotNone(matchRE.match(name))

    def doTestForExpectedMatchFailures(self, matchRE, names):
        for name in names:
            m = matchRE.match(name)
            self.assertIsNone(m)

    def doTestForExpectedExclusions(self, exRE):
        self.assertIsNotNone(exRE.match('foolish'))
        self.assertIsNotNone(exRE.match('superbar'))
        self.assertIsNotNone(exRE.match('junky'))
        self.assertIsNotNone(exRE.match('junkEverywhere')
                             )  # begins with 'junk'

    def testMakeExRE(self):
        """test utility for making excluded file name regexes"""
        exRE = self.makeExRE(None)
        self.assertTrue(exRE is not None)

        # should not be present
        self.assertTrue(None == exRE.match('bar'))
        self.assertTrue(None == exRE.match('foo'))

        exc = []
        exc.append('foo*')
        exc.append('*bar')
        exc.append('junk*')
        exRE = self.makeExRE(exc)
        self.doTestForExpectedExclusions(exRE)

        self.assertIsNotNone(exRE.match('foobarf'))
        self.assertIsNotNone(None == exRE.match(' foobarf'))
        self.assertIsNone(exRE.match(' foobarf'))

        self.assertIsNotNone(exRE.match('ohMybar'))

        self.assertIsNone(exRE.match('ohMybarf'))
        self.assertIsNotNone(exRE.match('junky'))
        self.assertIsNone(exRE.match(' junk'))           # GEEP

    def testMakeMatchRE(self):
        """test utility for making matched file name regexes"""
        matchRE = self.makeExRE(None)
        self.assertIsNotNone(matchRE)

        matches = []
        matches.append('foo*')
        matches.append('*bar')
        matches.append('junk*')
        matchRE = self.makeExRE(matches)
        self.doTestForExpectedMatches(matchRE,
                                      ['foo', 'foolish', 'roobar', 'junky'])
        self.doTestForExpectedMatchFailures(matchRE,
                                            [' foo', 'roobarf', 'myjunk'])
        #[ 'roobarf', 'myjunk'])

        matches = ['*.tgz']
        matchRE = self.makeExRE(matches)
        self.doTestForExpectedMatches(matchRE,
                                      ['junk.tgz', 'notSoFoolish.tgz'])
        self.doTestForExpectedMatchFailures(matchRE,
                                            ['junk.tar.gz', 'foolish.tar.gz'])

        matches = ['*.tgz', '*.tar.gz']
        matchRE = self.makeExRE(matches)
        self.doTestForExpectedMatches(matchRE,
                                      ['junk.tgz', 'notSoFoolish.tgz',
                                       'junk.tar.gz', 'ohHello.tar.gz'])
        self.doTestForExpectedMatchFailures(matchRE,
                                            ['junk.gz', 'foolish.tar'])

if __name__ == '__main__':
    unittest.main()
