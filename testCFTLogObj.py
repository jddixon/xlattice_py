#!/usr/bin/python3

# testCFTLogObj.py

import os
import time
import unittest
import sys
sys.path.insert(0, 'build/lib.linux-x86_64-2.7')  # for the .so
from cFTLogForPy import (
    initCFTLogger, closeCFTLogger, openCLog, logMsg)

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
        version = serverutil.__version__
        print("VERSION %s" % version, end=' ')
        if version >= '2.1.0':
            print(" %s" % serverutil.__version_date__)
            self.assertEquals(16, cFTLogForPy.max_log)
        else:
            print(" THIS IS AN OLD VERSION OF THE LIBRARY")

    def testCtor(self):
        status = initCFTLogger()
        logFile = self.uniqueFileName()
        obj = cFTLogForPy.FTLogForPy()
        obj.init(logFile)
        self.assertEquals(0, obj.ndx())
        self.assertEquals(0, obj.count())
        self.assertEquals(logFile, obj.logFile())

    def testCount(self):
        messages = ["now is the winter of our discontent\n",
                    "made glorious summer by this son of York\n",
                    "and all the clouds that lowered upon our house\n",
                    "... and so forth and so on\n",
                    ]
        logFile = self.uniqueFileName()
        # this 3-line stanza needs to be shortened
        status = initCFTLogger()
        obj = cFTLogForPy.FTLogForPy()
        obj.init(logFile)
        self.assertEquals(logFile, obj.logFile())       # must follow init()

        logNdx = obj.ndx()
        self.assertEquals(0, logNdx)
        expected = 0
        count = obj.count()
        self.assertEquals(expected, count)
        for msg in messages:
            obj.logMsg(msg)
            expected += 1
            count = obj.count()
            self.assertEquals(expected, count)

        # XXX OLD MODULE-LEVEL FUNC
        status = closeCFTLogger(logNdx)
        print("closeCFTLogger returns %s" % str(status))   # GEEP

if __name__ == '__main__':
    unittest.main()
