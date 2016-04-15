#!/usr/bin/python3

# testDecimalVersion.py

import sys
import time
import unittest
import rnglib

from xlattice.util import DecimalVersion, parseDecimalVersion


class TestDecimalVErsion (unittest.TestCase):

    def setUp(self):
        self.rng = rnglib.SimpleRNG(time.time())

    def tearDown(self):
        pass

    def testEmpty(self):
        try:
            dv1 = parseDecimalVersion(None)
            self.fail("parsed nil string")
        except RuntimeError:
            pass
        try:
            dv1 = parseDecimalVersion("")
            self.fail("parsed empty string")
        except RuntimeError:
            pass
        try:
            dv1 = parseDecimalVersion(" \t ")
            self.fail("parsed whitespace")
        except ValueError:
            pass

    def test4IntConstructor(self):
        dv1 = DecimalVersion(1, 2, 3, 4)
        s = dv1.__str__()
        self.assertEqual("1.2.3.4", s)
        self.assertEqual(dv1.getA(), 1)
        self.assertEqual(dv1.getB(), 2)
        self.assertEqual(dv1.getC(), 3)
        self.assertEqual(dv1.getD(), 4)
        dv2 = parseDecimalVersion(s)
        self.assertEqual(dv1.__eq__(dv2), True)
        self.assertEqual(dv1, dv2)

    def test3IntConstructor(self):
        dv1 = DecimalVersion(1, 2, 3)
        s = dv1.__str__()
        self.assertEqual("1.2.3", s)
        self.assertEqual(dv1.getA(), 1)
        self.assertEqual(dv1.getB(), 2)
        self.assertEqual(dv1.getC(), 3)
        self.assertEqual(dv1.getD(), 0)
        dv2 = parseDecimalVersion(s)
        self.assertEqual(dv1.__eq__(dv2), True)
        self.assertEqual(dv1, dv2)

    def test2IntConstructor(self):
        dv1 = DecimalVersion(1, 2)
        s = dv1.__str__()
        self.assertEqual("1.2.0", s)
        self.assertEqual(dv1.getA(), 1)
        self.assertEqual(dv1.getB(), 2)
        self.assertEqual(dv1.getC(), 0)
        self.assertEqual(dv1.getD(), 0)
        dv2 = parseDecimalVersion(s)
        self.assertEqual(dv1.__eq__(dv2), True)
        self.assertEqual(dv1, dv2)

    def test1IntConstructor(self):
        dv1 = DecimalVersion(1)
        s = dv1.__str__()
        self.assertEqual("1.0.0", s)
        self.assertEqual(dv1.getA(), 1)
        self.assertEqual(dv1.getB(), 0)
        self.assertEqual(dv1.getC(), 0)
        self.assertEqual(dv1.getD(), 0)
        dv2 = parseDecimalVersion(s)
        self.assertEqual(dv1.__eq__(dv2), True)
        self.assertEqual(dv1, dv2)

    def makeDecimalVersion(self):
        v = self.rng.nextInt32()
        a = 0xff & v
        b = 0xff & (v >> 8)
        c = 0xff & (v >> 16)
        d = 0xff & (v >> 24)
        dv = DecimalVersion(a, b, c, d)
        self.assertEqual(dv.value, v)
        self.assertEqual(a, dv.getA())
        self.assertEqual(b, dv.getB())
        self.assertEqual(c, dv.getC())
        self.assertEqual(d, dv.getD())

        return v, a, b, c, d, dv

    def testAssigningValues(self):
        v, a, b, c, d, dv = self.makeDecimalVersion()

        # test int assignment
        dv2 = DecimalVersion()
        dv2.value = v
        self.assertEqual(dv2.value, v)
        self.assertEqual(dv2, dv)

        # test str assignment
        dv3 = DecimalVersion()
        dv3.value = dv.__str__()
        self.assertEqual(dv3.value, v)
        self.assertEqual(dv3, dv)

        # test DecimalValue assignment
        dv4 = DecimalVersion()
        dv4.value = dv
        self.assertEqual(dv4.value, v)
        self.assertEqual(dv4, dv)

    def testSteppingMajor(self):
        v, a, b, c, d, dv = self.makeDecimalVersion()
        if a < 255:
            dv.stepMajor()
            self.assertEqual(dv.getA(), a + 1)
            self.assertEqual(dv.getB(), 0)
            self.assertEqual(dv.getC(), 0)
            self.assertEqual(dv.getD(), 0)
        else:
            try:
                dv.stepMajor()
                self.fail("didn't get exception stepping to 256")
            except RuntimeError:
                pass

    def testSteppingMinor(self):
        v, a, b, c, d, dv = self.makeDecimalVersion()
        if b < 255:
            dv.stepMinor()
            self.assertEqual(dv.getA(), a)
            self.assertEqual(dv.getB(), b + 1)
            self.assertEqual(dv.getC(), 0)
            self.assertEqual(dv.getD(), 0)
        else:
            try:
                dv.stepMinor()
                self.fail("didn't get exception stepping to 256")
            except RuntimeError:
                pass

    def testSteppingDecimal(self):
        v, a, b, c, d, dv = self.makeDecimalVersion()
        if c < 255:
            dv.stepDecimal()
            self.assertEqual(dv.getA(), a)
            self.assertEqual(dv.getB(), b)
            self.assertEqual(dv.getC(), c + 1)
            self.assertEqual(dv.getD(), 0)
        else:
            try:
                dv.stepDecimal()
                self.fail("didn't get exception stepping to 256")
            except RuntimeError:
                pass

    def testSteppingMicro(self):
        v, a, b, c, d, dv = self.makeDecimalVersion()
        if d < 255:
            dv.stepMicro()
            self.assertEqual(dv.getA(), a)
            self.assertEqual(dv.getB(), b)
            self.assertEqual(dv.getC(), c)
            self.assertEqual(dv.getD(), d + 1)
        else:
            try:
                dv.stepMicro()
                self.fail("didn't get exception stepping to 256")
            except RuntimeError:
                pass

    def testBooleans(self):

        # test __eq__()
        v1, a1, b1, c1, d1, dv1 = self.makeDecimalVersion()
        self.assertEqual(dv1, dv1)
        v2, a2, b2, c2, d2, dv2 = self.makeDecimalVersion()
        self.assertEqual(dv2, dv2)
        while v1 == v2:
            v2, a2, b2, c2, d2, dv2 = self.makeDecimalVersion()
            self.assertEqual(dv2, dv2)
        self.assertNotEqual(dv1, dv2)

        # test __lt__() ---------------------------------------------
        self.assertFalse(dv1 < dv1)
        self.assertFalse(dv2 < dv2)

        x = DecimalVersion(1, 2, 3, 4)
        y = DecimalVersion(1, 2, 3, 5)
        self.assertTrue(x < y)
        self.assertFalse(y < x)

        x = DecimalVersion(1, 2, 3, 4)
        y = DecimalVersion(1, 3, 4, 5)
        self.assertTrue(x < y)
        self.assertFalse(y < x)

        x = DecimalVersion(1, 2, 3, 4)
        y = DecimalVersion(2, 2, 4, 5)
        self.assertTrue(x < y)
        self.assertFalse(y < x)

        x = DecimalVersion(1, 2, 3, 4)
        y = DecimalVersion(1, 2, 4, 5)
        self.assertTrue(x < y)
        self.assertFalse(y < x)

        # test __le__() ---------------------------------------------
        self.assertTrue(dv1 <= dv1)
        self.assertTrue(dv2 <= dv2)

        x = DecimalVersion(1, 2, 3, 4)
        y = DecimalVersion(1, 2, 3, 5)
        self.assertTrue(x <= y)

        x = DecimalVersion(1, 2, 3, 4)
        y = DecimalVersion(1, 3, 4, 5)
        self.assertTrue(x <= y)

        x = DecimalVersion(1, 2, 3, 4)
        y = DecimalVersion(2, 2, 4, 5)
        self.assertTrue(x <= y)

        x = DecimalVersion(1, 2, 3, 4)
        y = DecimalVersion(1, 2, 4, 5)
        self.assertTrue(x <= y)

        # test __gt__() ---------------------------------------------
        self.assertFalse(dv1 > dv1)
        self.assertFalse(dv2 > dv2)

        x = DecimalVersion(1, 2, 3, 6)
        y = DecimalVersion(1, 2, 3, 5)
        self.assertTrue(x > y)
        self.assertFalse(y > x)

        x = DecimalVersion(1, 2, 5, 4)
        y = DecimalVersion(1, 2, 4, 5)
        self.assertTrue(x > y)
        self.assertFalse(y > x)

        x = DecimalVersion(1, 3, 5, 4)
        y = DecimalVersion(1, 2, 4, 5)
        self.assertTrue(x > y)
        self.assertFalse(y > x)

        x = DecimalVersion(2, 2, 3, 4)
        y = DecimalVersion(1, 2, 4, 5)
        self.assertTrue(x > y)
        self.assertFalse(y > x)

        # test __ge__() ---------------------------------------------
        self.assertTrue(dv1 >= dv1)
        self.assertTrue(dv2 >= dv2)

        x = DecimalVersion(1, 2, 3, 6)
        y = DecimalVersion(1, 2, 3, 5)
        self.assertTrue(x >= y)

        x = DecimalVersion(1, 2, 7, 4)
        y = DecimalVersion(1, 2, 4, 5)
        self.assertTrue(x >= y)

        x = DecimalVersion(1, 5, 3, 4)
        y = DecimalVersion(1, 2, 4, 5)
        self.assertTrue(x >= y)

        x = DecimalVersion(21, 2, 3, 4)
        y = DecimalVersion(1, 2, 4, 5)
        self.assertTrue(x >= y)

if __name__ == '__main__':
    unittest.main()
