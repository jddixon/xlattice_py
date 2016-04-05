#!/usr/bin/python3

# testCFTLogForPy.py
import os
import time
import unittest
import sys
import xlattice
sys.path.insert(0, 'build/lib.linux-x86_64-2.7')  # for the .so

from cFTLogForPy import (
    initCFTLogger, openCFTLog, logMsg, closeCFTLogger)

from rnglib import SimpleRNG


class TestCFTLogForPy (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())
        now = time.time()

    def tearDown(self):
        pass

    def uniqueFileName(self):
        logFile = "tmp/foo%04x" % self.rng.nextInt16()
        while os.path.exists(logFile):
            logFile = "tmp/foo%04x" % self.rng.nextInt16()
        return logFile

    # actual unit tests #############################################
    def testVersion(self):
        version = xlattice.__version__
        print("VERSION %s" % version, end=' ')
        if version >= '0.5.1':
            print(" %s" % xlattice.__version_date__)
        else:
            self.fail("have loaded an old version of the library")

    def testOpenAndClose(self):
        logFile = self.uniqueFileName()
        status = initCFTLogger()
        status = openCFTLog(logFile)
        self.assertEqual(0, status)
        time.sleep(0.2)
        if status:
            print("openCFTLog failed, status is %d" % status)
        else:
            time.sleep(0.2)
            status = closeCFTLogger()
        time.sleep(0.2)
        self.assertEqual(0, status)
        os.path.exists(logFile)

    class DumbLogger:

        def __init__(self):
            self.logFile = "tmp/dumb.log"

        def openLog(self):
            initCFTLogger()
            return openCFTLog(self.logFile)

        def closeLog(self):
            return closeCFTLogger()

    def testDumbLogger(self):
        logger = self.DumbLogger()
        time.sleep(0.1)
        status = logger.openLog()
        self.assertEqual(0, status)
        time.sleep(0.1)
        status = logger.closeLog()
        time.sleep(0.1)
        self.assertEqual(0, status)
        self.assertTrue(os.path.exists(logger.logFile))

    def testInitialization(self):
        """tests init, log messages, close, with sleeps"""
        logFile = self.uniqueFileName()
        status = initCFTLogger()
        logNdx = openCFTLog(logFile)
        if logNdx:
            print("openCFTLogger failed, logNdx is %d" % logNdx)
        else:
            logMsg(logNdx, "now is the winter of our discontent\n")
            logMsg(logNdx, "made glorious summer by this son of York\n")
            logMsg(logNdx, "buffers are temporarily multiples of 64B\n")
            logMsg(logNdx, "... so these few message should overflow a page\n")
            # print "ABOUT TO WRITE BLOCK 0";    sys.stdout.flush()
            for n in range(128):
                #       ....x....1....x....2....x....3....x....4...
                logMsg(
                    logNdx,
                    "padding ljlkjk;ljlj;k;lklj;j;kjkljklj %04x\n" %
                    n)
                # we see 0 .. 87 consistently, so 88 * 43 = 3784 bytes
                # have been written and the next line would take it to
                # print '%3d' % n, ; sys.stdout.flush()     # DEBUG
            # print # DEBUG

            # print "BLOCK 0 WRITTEN";    sys.stdout.flush()
            time.sleep(0.2)     # NOTE
            for n in range(128):
                logMsg(
                    logNdx, "padding ljlkjk;ljlj;k;lklj;j;kjkljklj %04x\n" %
                    (n + 128))
            # print "BLOCK 1 WRITTEN";    sys.stdout.flush()
            time.sleep(0.2)     # NOTE
            for n in range(128):
                logMsg(
                    logNdx, "padding ljlkjk;ljlj;k;lklj;j;kjkljklj %04x\n" %
                    (n + 256))
            # print "BLOCK 2 WRITTEN";    sys.stdout.flush()
            time.sleep(0.2)     # NOTE
            for n in range(128):
                logMsg(
                    logNdx, "padding ljlkjk;ljlj;k;lklj;j;kjkljklj %04x\n" %
                    (n + 384))
            # print "BLOCK 3 WRITTEN";    sys.stdout.flush()
            # closeCFTLogger(None)

            # print "BRANCHING TO closeCFTLogger"; sys.stdout.flush()   # NOT
            # :1SEEN
            junk = closeCFTLogger()
            # print "closeCFTLogger returns %s" % str(junk);
            # sys.stdout.flush()

            time.sleep(0.2)     # NOTE_AT_END

if __name__ == '__main__':
    unittest.main()
