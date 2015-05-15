# xlattice_py/xlattice/xlutil.py

import calendar, time

__all__ = ['TIMESTAMP_FORMAT',
           'DecimalVersion', 'parseDecimalVersion',
           'parseTimestamp', 'timestamp', 'timestampNow', 
          ]

# DECIMAL VERSION ---------------------------------------------------

class DecimalVersion(object):

    # __slots__ = ['_value',]

    def __init__(self, aIn, bIn=None, cIn=None, dIn=None):
        if aIn == None:
            raise RuntimeError("Nil major version")
        a = int(aIn)
        if a < 0 or 255 < a:
            raise RuntimeError("version number part a '%d' out of range" % a)
        if bIn == None:
            b = 0
        else:
            b = int(bIn)
            if b < 0 or 255 < b:
                raise RuntimeError("version part b '%d' out of range" % b)
        if cIn == None:
            c = 0
        else:
            c = int(cIn)
            if c < 0 or 255 < c:
                raise RuntimeError("version part c '%d' out of range" % c)
        if dIn == None:
            d = 0
        else:
            d = int(dIn)
            if d < 0 or 255 < d:
                raise RuntimeError("version part d '%d' out of range" % d)

        self._value = (0xff & a)         | ((0xff & b) << 8)  |  \
                     ((0xff & c) << 16) | ((0xff & d) << 24)


    def getA(self):
        return self._value & 0xff
    def getB(self):
        return (self._value >> 8) & 0xff
    def getC(self):
        return (self._value >> 16) & 0xff
    def getD(self):
        return (self._value >> 24) & 0xff

   
    @property
    def value(self):
        return self._value

    def __eq__ (self, other):

        if type(other) != DecimalVersion:
            return False
        return self._value == other._value

    def __str__(self):
        a = self.getA()
        b = self.getB()
        c = self.getC()
        d = self.getD()
        if d != 0:
            s = "%d.%d.%d.%d" % (a,b,c,d)
        elif c != 0:
            s = "%d.%d.%d" % (a,b,c)
        else:
            s = "%d.%d" % (a,b)
        return s

def parseDecimalVersion(s):
    """
    Expect the parameter s to be a string looking like a.b.c.d or a 
    shorter version.  Returns a DecimalVersion object.
    """

    if s == None or s=="":
        raise RuntimeError("nil or empty version string")

    dv = None
    ss = s.split(".")
    length = len(ss)
    if length == 1:
        dv = DecimalVersion(ss[0])
    elif length == 2:
        dv = DecimalVersion(ss[0], ss[1])
    elif length == 3:
        dv = DecimalVersion(ss[0], ss[1], ss[2])
    elif length == 4:
        dv = DecimalVersion(ss[0], ss[1], ss[2], ss[3])
    else:
        raise RuntimeError("not a well-formed DecimalVersion: '%s'" % s)
    return dv

# TIMESTAMP FUNCTIONS -----------------------------------------------

# Note that in the Go code timestamp is an int64, whereas here it
# is a string.
# Note also that these functions will misbehave from 2038 or so.

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

def parseTimestamp(s):
    """ May raise ValueError """
    t = time.strptime(s, TIMESTAMP_FORMAT)
    return calendar.timegm(t)

def timestamp(n):       # sec from epoch
    t = time.gmtime(n)
    return time.strftime(TIMESTAMP_FORMAT,  t)

def timestampNow():
    t = time.gmtime()
    return time.strftime(TIMESTAMP_FORMAT,  t)

