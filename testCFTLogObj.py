#!/usr/bin/python3

# testCFTLogObj.py

import os
import sys
import time
import unittest
import xlattice
sys.path.insert(0, 'build/lib.linux-x86_64-3.4')  # for the .so

import cFTLogForPy
from cFTLogForPy import (
    initCFTLogger, closeCFTLogger, openCFTLog, logMsg)

from rnglib import SimpleRNG


class TestCLogObj (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())
        now = time.time()

    def tearDown(self):
        pass

    # utility functions #############################################
    def uniqueFileName(self):
        logFile = "tmp/foo%04x" % self.rng.nextInt16()
        while os.path.exists(logFile):
            logFile = "tmp/foo%04x" % self.rng.nextInt16()
        return logFile

    # actual unit tests #############################################
    def testVersionAndMaxLog(self):
        version = xlattice.__version__
        print("VERSION %s" % version, end=' ')
        if version >= '0.5.1':
            print(" %s" % xlattice.__version_date__)
            self.assertEqual(16, cFTLogForPy.max_log)
        else:
            print(" THIS IS AN OLD VERSION OF THE LIBRARY")

    def testCtor(self):
        status = initCFTLogger()
        logFile = self.uniqueFileName()
        obj = cFTLogForPy.LogForPy()
        obj.init(logFile)
        self.assertEqual(0, obj.ndx())
        self.assertEqual(0, obj.count())
        self.assertEqual(logFile, obj.logFile())

    def testCount(self):
        messages = ["now is the winter of our discontent\n",
                    "made glorious summer by this son of York\n",
                    "and all the clouds that lowered upon our house\n",
                    "... and so forth and so on\n",
                    ]
        logFile = self.uniqueFileName()
        # this 3-line stanza needs to be shortened
        status = initCFTLogger()
        obj = cFTLogForPy.LogForPy()
        obj.init(logFile)
        self.assertEqual(logFile, obj.logFile())       # must follow init()

        logNdx = obj.ndx()
        self.assertEqual(0, logNdx)
        expected = 0
        count = obj.count()
        self.assertEqual(expected, count)
        for msg in messages:
            obj.logMsg(msg)
            expected += 1
            count = obj.count()
            self.assertEqual(expected, count)

        # XXX OLD MODULE-LEVEL FUNC
        status = closeCFTLogger(logNdx)
        # print("closeCFTLogger returns %s" % str(status))   # GEEP
        self.assertEqual(status, 0)

if __name__ == '__main__':
    unittest.main()
