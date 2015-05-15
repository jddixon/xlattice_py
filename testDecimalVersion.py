#!/usr/bin/python3

# testDecimalVersion.py

import  sys, unittest
from xlReg import decimalVersion as dv

class TestDecimalVErsion (unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def testEmpty(self):
        try:
            dv1 = dv.parseDecimalVersion(None)
            self.fail("parsed nil string")
        except RuntimeError: 
            pass
        try:
            dv1 = dv.parseDecimalVersion("")
            self.fail("parsed empty string")
        except RuntimeError: 
            pass
        try:
            dv1 = dv.parseDecimalVersion(" \t ")
            self.fail("parsed whitespace")
        except ValueError: 
            pass


    def test4IntConstructor(self):
        dv1 = dv.DecimalVersion(1,2,3,4)
        s = dv1.__str__();
        self.assertEqual("1.2.3.4", s)
        self.assertEqual(dv1.getA(), 1)
        self.assertEqual(dv1.getB(), 2)
        self.assertEqual(dv1.getC(), 3)
        self.assertEqual(dv1.getD(), 4)
        dv2 = dv.parseDecimalVersion(s)
        self.assertEqual(dv1.__eq__(dv2), True)
        self.assertEqual(dv1, dv2)

    def test3IntConstructor(self):
        dv1 = dv.DecimalVersion(1,2,3)
        s = dv1.__str__();
        self.assertEqual("1.2.3", s)
        self.assertEqual(dv1.getA(), 1)
        self.assertEqual(dv1.getB(), 2)
        self.assertEqual(dv1.getC(), 3)
        self.assertEqual(dv1.getD(), 0)
        dv2 = dv.parseDecimalVersion(s)
        self.assertEqual(dv1.__eq__(dv2), True)
        self.assertEqual(dv1, dv2)

    def test2IntConstructor(self):
        dv1 = dv.DecimalVersion(1,2)
        s = dv1.__str__();
        self.assertEqual("1.2", s)
        self.assertEqual(dv1.getA(), 1)
        self.assertEqual(dv1.getB(), 2)
        self.assertEqual(dv1.getC(), 0)
        self.assertEqual(dv1.getD(), 0)
        dv2 = dv.parseDecimalVersion(s)
        self.assertEqual(dv1.__eq__(dv2), True)
        self.assertEqual(dv1, dv2)

    def test1IntConstructor(self):
        dv1 = dv.DecimalVersion(1)
        s = dv1.__str__();
        self.assertEqual("1.0", s)
        self.assertEqual(dv1.getA(), 1)
        self.assertEqual(dv1.getB(), 0)
        self.assertEqual(dv1.getC(), 0)
        self.assertEqual(dv1.getD(), 0)
        dv2 = dv.parseDecimalVersion(s)
        self.assertEqual(dv1.__eq__(dv2), True)
        self.assertEqual(dv1, dv2)

if __name__ == '__main__':
    unittest.main()
