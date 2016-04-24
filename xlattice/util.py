# xlattice_py/xlattice/util.py

import calendar
import fnmatch
import os
import re
import time

__all__ = ['TIMESTAMP_FORMAT',
           'DecimalVersion', 'parseDecimalVersion',
           'parseTimestamp', 'timestamp', 'timestampNow',

           'getExclusions', 'makeExRE', 'regexesFromWildcards',
           ]

# DECIMAL VERSION ---------------------------------------------------


class DecimalVersion(object):

    # __slots__ = ['_value',]

    def __init__(self, aIn=None, bIn=None, cIn=None, dIn=None):
        if aIn is None:
            aIn = 0
        a = int(aIn)
        if a < 0 or 255 < a:
            raise RuntimeError("version number part a '%d' out of range" % a)
        if bIn is None:
            b = 0
        else:
            b = int(bIn)
            if b < 0 or 255 < b:
                raise RuntimeError("version part b '%d' out of range" % b)
        if cIn is None:
            c = 0
        else:
            c = int(cIn)
            if c < 0 or 255 < c:
                raise RuntimeError("version part c '%d' out of range" % c)
        if dIn is None:
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

    @value.setter
    def value(self, val):
        if isinstance(val, int):
            self._value = val
        elif isinstance(val, str):
            self._value = parseDecimalVersion(val).value
        elif isinstance(val, DecimalVersion):
            self._value = val.value
        else:
            raise RuntimeError("Don't know how to assign '%s' as a value" % (
                val))

    def __eq__(self, other):

        if not isinstance(other, DecimalVersion):
            return False
        return self._value == other._value

    def __lt__(self, other):
        sA = self.getA()
        oA = other.getA()
        if sA < oA:
            return True
        if sA > oA:
            return False

        sB = self.getC()
        oB = other.getC()
        if sB < oB:
            return True
        if sB > oB:
            return False

        sC = self.getC()
        oC = other.getC()
        if sC < oC:
            return True
        if sC > oC:
            return False

        sD = self.getD()
        oD = other.getD()
        if sD < oD:
            return True
        return False

        if self.getA() < other.getA():
            return False
        if self.getB() < other.getB():
            return False
        if self.getC() < other.getC():
            return False
        if self.getD() <= other.getD():
            return False
        return True

    def __le__(self, other):
        sA = self.getA()
        oA = other.getA()
        if sA < oA:
            return True
        if sA > oA:
            return False

        sB = self.getB()
        oB = other.getB()
        if sB < oB:
            return True
        if sB > oB:
            return False

        sC = self.getC()
        oC = other.getC()
        if sC < oC:
            return True
        if sC > oC:
            return False

        sD = self.getD()
        oD = other.getD()
        if sD <= oD:
            return True
        return False
        if self.getA() < other.getA():
            return False
        if self.getB() < other.getB():
            return False
        if self.getC() < other.getC():
            return False
        if self.getD() < other.getD():
            return False
        return True

    def __gt__(self, other):
        sA = self.getA()
        oA = other.getA()
        if sA > oA:
            return True
        if sA < oA:
            return False

        sB = self.getC()
        oB = other.getC()
        if sB > oB:
            return True
        if sB < oB:
            return False

        sC = self.getC()
        oC = other.getC()
        if sC > oC:
            return True
        if sC < oC:
            return False

        sD = self.getD()
        oD = other.getD()
        if sD > oD:
            return True
        return False

    def __ge__(self, other):
        sA = self.getA()
        oA = other.getA()
        if sA > oA:
            return True
        if sA < oA:
            return False

        sB = self.getB()
        oB = other.getB()
        if sB > oB:
            return True
        if sB < oB:
            return False

        sC = self.getC()
        oC = other.getC()
        if sC > oC:
            return True
        if sC < oC:
            return False

        sD = self.getD()
        oD = other.getD()
        if sD >= oD:
            return True
        return False

    def __str__(self):
        a = self.getA()
        b = self.getB()
        c = self.getC()
        d = self.getD()
        if d != 0:
            s = "%d.%d.%d.%d" % (a, b, c, d)
        else:
            s = "%d.%d.%d" % (a, b, c)
        return s

    def stepMajor(self):
        """
        Increment the major part of the version number, the A in a.b.c.d.
        This clears (zeroes out) the other three fields.
        """
        a = self.getA()
        a += 1
        if a > 255:
            raise RuntimeError("stepMajor() takes it out of range")
        else:
            self.value = DecimalVersion(a)

    def stepMinor(self):
        """
        Increment the minor part of the version number, the B in a.b.c.d.
        This zeroes out the 'decimal' and 'micro' fields.
        """
        a = self.getA()
        b = self.getB()
        b += 1
        if b > 255:
            raise RuntimeError("stepMinor() takes it out of range")
        else:
            self.value = DecimalVersion(a, b)

    def stepDecimal(self):
        """
        Increment the decimal part of the version number, the C in a.b.c.d.
        This clears the 4th 'micro' field.
        """
        a = self.getA()
        b = self.getB()
        c = self.getC()
        c += 1
        if c > 255:
            raise RuntimeError("stepDecimal() takes it out of range")
        else:
            self.value = DecimalVersion(a, b, c)

    def stepMicro(self):
        """
        Increment the micro part of the version number, the D in a.b.c.d.
        This leaves the other three fields unaffected.
        """
        a = self.getA()
        b = self.getB()
        c = self.getC()
        d = self.getD()
        d += 1
        if d > 255:
            raise RuntimeError("stepMicro() takes it out of range")
        else:
            self.value = DecimalVersion(a, b, c, d)


def parseDecimalVersion(s):
    """
    Expect the parameter s to be a string looking like a.b.c.d or a
    shorter version.  Returns a DecimalVersion object.
    """

    if s is None or s == "":
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

# %T is shorthand for %H:%M:%S
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def parseTimestamp(s):
    """
    If there is a decimal part to the seconds field, will raise ValueError
    with the message 'unconverted data remains: .123456'.
    """
    t = time.strptime(s, TIMESTAMP_FORMAT)
    return calendar.timegm(t)


def timestamp(n):       # sec from epoch
    """
    Given n the number of seconds from the epoch, return a string in
    the shorter format.  This truncates microseconds from the time.
    """
    t = time.gmtime(n)
    return time.strftime(TIMESTAMP_FORMAT, t)


def timestampNow():
    """
    Get the current time, truncate it by omiting microseconds, and
    return a string in the shorter format.
    """
    t = time.gmtime()
    return time.strftime(TIMESTAMP_FORMAT, t)

# GLOBS, WILDCARDS --------------------------------------------------


def getExclusions(projDir, exclFile='.gitignore'):
    """
    projDir must exist and may contain a .gitignore file containing one
    or more globs.

    Returns the contents of exclusion file (.girignore by default) as a
    list.  The list may be empty.  Any lines in the list are guaranteed
    be have had leading and trailing spaces stripped and will be
    non-empty.
    """

    globs = []
    pathToIgnore = os.path.join(projDir, exclFile)
    if os.path.isfile(pathToIgnore):
        with open(pathToIgnore, 'rb') as f:
            data = f.read().decode('utf8')
        if data:
            lines = data.split('\n')
            for line in lines:
                line = line.strip()
                if line:
                    globs.append(line)
    return globs


def makeExRE(globs):
    """
    Given a list of globs aka wildcards, return a compiled regular
    expression representing a match on one or more globs.  That is,
    we convert the wildcards to regular expressions, OR them all
    together, and compile and return the result.
    """
    r = regexesFromWildcards(globs)
    return re.compile('|'.join(r))


def regexesFromWildcards(ss):
    """
    Given a list of wildcards, return a list of parenthesized
    regular expressions.
    """
    r = []
    if ss:
        for glob in ss:
            glob = glob.strip()
            # ignore empty wildcards
            if glob:
                # \Z means end of string, (?ms) means accept either
                # the M multiline flag or S, which makes . expand
                pat = fnmatch.translate(glob)
                r.append('(' + pat + ')')
    else:
        r.append('a^')      # matches nothing

    return r
