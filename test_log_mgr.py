#!/usr/bin/env python3

# xlattice_py/testLogMgr.py

import hashlib
import os
import re
import shutil
import time
import unittest
import sys
from xlattice.ftLog import LogMgr
sys.path.insert(0, 'build/lib.linux-x86_64-3.4')  # for the .so


class TestLogMgr (unittest.TestCase):

    def setUp(self):
        now = time.time()

    def tearDown(self):
        pass

    # utility functions #############################################

    # actual unit tests #############################################
    def testJustOpenAndClose(self):
        if os.path.exists('./logs'):
            shutil.rmtree('./logs')
        mgr = LogMgr('logs')
        logger = mgr.open('foo')
        self.assertIsNotNone(logger)
        # print "XXX NO MESSAGES XXX"
        expectedLogFile = 'logs/foo.log'
        self.assertEqual(expectedLogFile, logger.logFileName)
        # we don't provide any way to close individual logs
        mgr.close()

        contents = None
        with open(expectedLogFile, 'r') as f:
            contents = f.read()
        if contents:
            contents = contents.strip()
            self.assertEqual(0, len(contents))

    def testWithSingleMessage(self):
        if os.path.exists('./logs'):
            shutil.rmtree('./logs')
        mgr = LogMgr('logs')
        logger = mgr.open('foo')
        logger.log('oh hello')
        # can't test this after logger closed - because object destroyes
        expectedLogFile = 'logs/foo.log'
        self.assertEqual(expectedLogFile, logger.logFileName)
        mgr.close()

        self.assertTrue(os.path.exists(expectedLogFile))
        with open(expectedLogFile, 'r') as f:
            contents = f.read()
        contents = contents.strip()
        self.assertTrue(contents.endswith('oh hello'))    # GEEP

    def testMoreMessages(self):
        if os.path.exists('./logs'):
            shutil.rmtree('./logs')
        mgr = LogMgr('logs')
        logger = mgr.open('bar')
        msg = ''
        msg += logger.log("this is gibberish ending in uhm lots of stuff and A")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and B")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and C")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and D")
        expectedLogFile = 'logs/bar.log'
        self.assertEqual(expectedLogFile, logger._logFile)
        mgr.close()

        self.assertTrue(os.path.exists(expectedLogFile))
        with open(expectedLogFile, 'r') as f:
            contents = f.read()
        self.assertEqual(msg, contents)          # END

    def testMessagesWithSleeps(self):
        # The presence of a time.sleep() _anywhere_ in the method used
        # to cause a segfault
        if os.path.exists('./logs'):
            shutil.rmtree('./logs')
        mgr = LogMgr('logs')
        logger = mgr.open('baz')
        msg = ''
        msg += logger.log("this is gibberish ending in uhm lots of stuff and A")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and B")
        time.sleep(0.2)
        msg += logger.log("this is gibberish ending in uhm lots of stuff and C")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and D")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and E")
        time.sleep(0.2)
        msg += logger.log("this is gibberish ending in uhm lots of stuff and F")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and G")
        msg += logger.log("this is gibberish ending in uhm lots of stuff and H")
        time.sleep(0.2)
        expectedLogFile = 'logs/baz.log'
        self.assertEqual(expectedLogFile, logger._logFile)
        mgr.close()

        self.assertTrue(os.path.exists(expectedLogFile))
        with open(expectedLogFile, 'r') as f:
            contents = f.read()
        self.assertEqual(msg, contents)      # FOOFOO

if __name__ == '__main__':
    unittest.main()
