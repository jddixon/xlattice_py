#!/usr/bin/env python3

# testLibev.py

import os
import time
import unittest
import pyev
import signal

import sys
sys.path.insert(0, 'build/lib.linux-x86_64-2.7')  # for the .so
from rnglib import SimpleRNG


def sig_cb(watcher, revenets):
    print("\n<KEYBOARD INTERRUPT>")
    loop = watcher.loop
    loop.stop(pyev.EVBREAK_ALL)


def guillotine_cb(watcher, revents):
    watcher.loop.stop(pyev.EVBREAK_ALL)


def timer_cb(watcher, revents):
    # right out of the book
    watcher.data += 1
    print("timer.data: {0}".format(watcher.data))
    print("timer.loop.iteration: {0}".format(watcher.loop.iteration))
    print("timer.loop.now(): {0}".format(watcher.loop.now()))

TICK = 0.051
LIFETIME = 1.720


class TestLibev (unittest.TestCase):

    def setUp(self):
        self.rng = SimpleRNG(time.time())
        now = time.time()
        self.loop = None
        self.logName = None
        self.fd = None

    def tearDown(self):
        if self.loop:
            self.loop.stop()

    # utility functions #############################################

    def setupAsyncLogging(self):
        self.loop = pyev.default_loop()
        self.logName = 'tmp/log%05x' % self.rng.nextInt32(1024 * 1024)
        self.fd = os.open(self.logName,
                          os.O_CREAT | os.O_APPEND | os.O_NONBLOCK,   # flags
                          0o644)                                       # mode

        # set up watchers ##################################
        # ticks every second
        timer = self.loop.timer(0, TICK, timer_cb, 0)
        timer.start()

        # kills the event loop after LIFETIME seconds
        lifeIsShort = self.loop.timer(LIFETIME, 0, guillotine_cb, 0)
        lifeIsShort.start()

        # lets the keyboard end things early
        sigHandler = self.loop.signal(signal.SIGINT, sig_cb)
        sigHandler.start()

        self.loop.start()

    # actual unit tests #############################################

    def testAsyncLog(self):
        t0 = time.time()
        self.setupAsyncLogging()
        t1 = time.time()
        deltaT = 1.0 * (t1 - t0)
        self.assertTrue(deltaT >= LIFETIME and deltaT < LIFETIME + 0.005)

if __name__ == '__main__':
    unittest.main()
