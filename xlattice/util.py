# xlattice_py/xlattice/util.py

import calendar
import fnmatch
import os
import re
import time

__all__ = ['TIMESTAMP_FORMAT',
           'DecimalVersion', 'timestamp',

           'parse_decimal_version', 'parse_timestamp', 'timestamp_now',
           'get_exclusions', 'make_ex_re', 'make_match_re', 'regexes_from_wildcards',

           # SYNONYMS, to be dropped ASAP
           'parseDecimalVersion', 'parseTimestamp', 'timestampNow',
           'getExclusions', 'makeExRE', 'makeMatchRE', 'regexesFromWildcards',
           ]

# SYNONYMS ----------------------------------------------------------


def parseDecimalVersion(line):
    """ SYNONYM """
    return parse_decimal_version(line)


def parseTimestamp(line):
    """ SYNONYM """
    return parse_timestamp(line)


def timestampNow():
    """ SYNONYM """
    return timestamp_now()


def getExclusions(projDir, exclFile='.gitignore'):
    """ SYNONYM """
    return get_exclusions(projDir, exclFile)


def makeExRE(globs):
    """ SYNONYM """
    return make_ex_re(globs)


def makeMatchRE(matchList):
    """ SYNONYM """
    return make_match_re(matchList)


def regexesFromWildcards(lines):
    """ SYNONYM """
    return regexes_from_wildcards(lines)

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

    # SYNONYMS
    def getA(self):
        """ SYNONYM """
        return self.get_a()

    def getB(self):
        """ SYNONYM """
        return self.get_b()

    def getC(self):
        """ SYNONYM """
        return self.get_c()

    def getD(self):
        """ SYNONYM """
        return self.get_d()
    # END SYNONYMS

    def get_a(self):
        return self._value & 0xff

    def get_b(self):
        return (self._value >> 8) & 0xff

    def get_c(self):
        return (self._value >> 16) & 0xff

    def get_d(self):
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
        sA = self.get_a()
        oA = other.get_a()
        if sA < oA:
            return True
        if sA > oA:
            return False

        sB = self.get_c()
        oB = other.get_c()
        if sB < oB:
            return True
        if sB > oB:
            return False

        sC = self.get_c()
        oC = other.get_c()
        if sC < oC:
            return True
        if sC > oC:
            return False

        sD = self.get_d()
        oD = other.get_d()
        if sD < oD:
            return True
        return False

        if self.get_a() < other.get_a():
            return False
        if self.get_b() < other.get_b():
            return False
        if self.get_c() < other.get_c():
            return False
        if self.get_d() <= other.get_d():
            return False
        return True

    def __le__(self, other):
        sA = self.get_a()
        oA = other.get_a()
        if sA < oA:
            return True
        if sA > oA:
            return False

        sB = self.get_b()
        oB = other.get_b()
        if sB < oB:
            return True
        if sB > oB:
            return False

        sC = self.get_c()
        oC = other.get_c()
        if sC < oC:
            return True
        if sC > oC:
            return False

        sD = self.get_d()
        oD = other.get_d()
        if sD <= oD:
            return True
        return False
        if self.get_a() < other.get_a():
            return False
        if self.get_b() < other.get_b():
            return False
        if self.get_c() < other.get_c():
            return False
        if self.get_d() < other.get_d():
            return False
        return True

    def __gt__(self, other):
        sA = self.get_a()
        oA = other.get_a()
        if sA > oA:
            return True
        if sA < oA:
            return False

        sB = self.get_c()
        oB = other.get_c()
        if sB > oB:
            return True
        if sB < oB:
            return False

        sC = self.get_c()
        oC = other.get_c()
        if sC > oC:
            return True
        if sC < oC:
            return False

        sD = self.get_d()
        oD = other.get_d()
        if sD > oD:
            return True
        return False

    def __ge__(self, other):
        sA = self.get_a()
        oA = other.get_a()
        if sA > oA:
            return True
        if sA < oA:
            return False

        sB = self.get_b()
        oB = other.get_b()
        if sB > oB:
            return True
        if sB < oB:
            return False

        sC = self.get_c()
        oC = other.get_c()
        if sC > oC:
            return True
        if sC < oC:
            return False

        sD = self.get_d()
        oD = other.get_d()
        if sD >= oD:
            return True
        return False

    def __str__(self):
        a = self.get_a()
        b = self.get_b()
        c = self.get_c()
        d = self.get_d()
        if d != 0:
            s = "%d.%d.%d.%d" % (a, b, c, d)
        else:
            s = "%d.%d.%d" % (a, b, c)
        return s

    # SYNONYM
    def stepMajor(self): return self.step_major()

    def stepMinor(self): return self.step_minor()

    def stepDecimal(self): return self.step_decimal()

    def stepMicro(self): return self.step_micro()
    # END SYN

    def step_major(self):
        """
        Increment the major part of the version number, the A in a.b.c.d.
        This clears (zeroes out) the other three fields.
        """
        a = self.get_a()
        a += 1
        if a > 255:
            raise RuntimeError("stepMajor() takes it out of range")
        else:
            self.value = DecimalVersion(a)

    def step_minor(self):
        """
        Increment the minor part of the version number, the B in a.b.c.d.
        This zeroes out the 'decimal' and 'micro' fields.
        """
        a = self.get_a()
        b = self.get_b()
        b += 1
        if b > 255:
            raise RuntimeError("stepMinor() takes it out of range")
        else:
            self.value = DecimalVersion(a, b)

    def step_decimal(self):
        """
        Increment the decimal part of the version number, the C in a.b.c.d.
        This clears the 4th 'micro' field.
        """
        a = self.get_a()
        b = self.get_b()
        c = self.get_c()
        c += 1
        if c > 255:
            raise RuntimeError("stepDecimal() takes it out of range")
        else:
            self.value = DecimalVersion(a, b, c)

    def step_micro(self):
        """
        Increment the micro part of the version number, the D in a.b.c.d.
        This leaves the other three fields unaffected.
        """
        a = self.get_a()
        b = self.get_b()
        c = self.get_c()
        d = self.get_d()
        d += 1
        if d > 255:
            raise RuntimeError("stepMicro() takes it out of range")
        else:
            self.value = DecimalVersion(a, b, c, d)


def parse_decimal_version(s):
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


def parse_timestamp(s):
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


def timestamp_now():
    """
    Get the current time, truncate it by omiting microseconds, and
    return a string in the shorter format.
    """
    t = time.gmtime()
    return time.strftime(TIMESTAMP_FORMAT, t)

# GLOBS, WILDCARDS --------------------------------------------------


def get_exclusions(projDir, exclFile='.gitignore'):
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


def make_ex_re(globs):
    """
    Given a list of globs aka wildcards, return a compiled regular
    expression representing a match on one or more globs.  That is,
    we convert the wildcards to regular expressions, OR them all
    together, and compile and return the result.
    """
    r = regexesFromWildcards(globs)
    return re.compile('|'.join(r))


def make_match_re(matchList):
    """
    Given a list of globs aka wildcards, return a compiled regular
    expression representing a match on one or more globs.  That is,
    we convert the wildcards to regular expressions, OR them all
    together, and compile and return the result.
    """
    return makeExRE(matchList)


def regexes_from_wildcards(ss):
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
