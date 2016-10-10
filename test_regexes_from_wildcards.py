#!/usr/bin/env python3

# testRegexesFromWildcards.py

import hashlib
import os
import re
import shutil
import time
import unittest
from rnglib import SimpleRNG
from xlattice.util import makeExRE, makeMatchRE, regexesFromWildcards


class TestRegexesFromWildcards (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())

    def tearDown(self):
        pass

    # utility functions #############################################

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
        self.assertIsNotNone(exRE.match('.merkle'))
        self.assertIsNotNone(exRE.match('foo.pyc'))

    def testMakeExRE(self):
        """test utility for making excluded file name regexes"""
        exRE = makeExRE(None)
        self.assertTrue(exRE is not None)

        # should not be present
        self.assertTrue(None == exRE.match('bar'))
        self.assertTrue(None == exRE.match('foo'))

        exc = []
        exc.append('foo*')
        exc.append('*bar')
        exc.append('junk*')
        exc.append('.merkle')
        exc.append('*.pyc')
        exRE = makeExRE(exc)
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
        matchRE = makeMatchRE(None)
        self.assertIsNotNone(matchRE)

        matches = []
        matches.append('foo*')
        matches.append('*bar')
        matches.append('junk*')
        matchRE = makeMatchRE(matches)
        self.doTestForExpectedMatches(matchRE,
                                      ['foo', 'foolish', 'roobar', 'junky'])
        self.doTestForExpectedMatchFailures(matchRE,
                                            [' foo', 'roobarf', 'myjunk'])
        #[ 'roobarf', 'myjunk'])

        matches = ['*.tgz']
        matchRE = makeMatchRE(matches)
        self.doTestForExpectedMatches(matchRE,
                                      ['junk.tgz', 'notSoFoolish.tgz'])
        self.doTestForExpectedMatchFailures(matchRE,
                                            ['junk.tar.gz', 'foolish.tar.gz'])

        matches = ['*.tgz', '*.tar.gz']
        matchRE = makeMatchRE(matches)
        self.doTestForExpectedMatches(matchRE,
                                      ['junk.tgz', 'notSoFoolish.tgz',
                                       'junk.tar.gz', 'ohHello.tar.gz'])
        self.doTestForExpectedMatchFailures(matchRE,
                                            ['junk.gz', 'foolish.tar'])

if __name__ == '__main__':
    unittest.main()
