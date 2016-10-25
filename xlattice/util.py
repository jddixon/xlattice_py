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
           # SYNONYMS, restored
           'parseDecimalVersion', 'parseTimestamp', 'timestampNow',
           'getExclusions', 'makeExRE', 'makeMatchRE', 'regexesFromWildcards',
           # END SYN
           ]

# DECIMAL VERSION ---------------------------------------------------


class DecimalVersion(object):

    # __slots__ = ['_value',]

    def __init__(self, aIn=None, bIn=None, cIn=None, dIn=None):
        if aIn is None:
            aIn = 0
        a_val = int(aIn)
        if a_val < 0 or 255 < a_val:
            raise RuntimeError(
                "version number part a '%d' out of range" %
                a_val)
        if bIn is None:
            b_val = 0
        else:
            b_val = int(bIn)
            if b_val < 0 or 255 < b_val:
                raise RuntimeError("version part b '%d' out of range" % b_val)
        if cIn is None:
            c_val = 0
        else:
            c_val = int(cIn)
            if c_val < 0 or 255 < c_val:
                raise RuntimeError("version part c '%d' out of range" % c_val)
        if dIn is None:
            d_val = 0
        else:
            d_val = int(dIn)
            if d_val < 0 or 255 < d_val:
                raise RuntimeError("version part d '%d' out of range" % d_val)

        self._value = (0xff & a_val)         | ((0xff & b_val) << 8)  |\
            ((0xff & c_val) << 16) | ((0xff & d_val) << 24)

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
            self._value = parse_decimal_version(val).value
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
        self_a = self.get_a()
        other_a = other.get_a()
        if self_a < other_a:
            return True
        if self_a > other_a:
            return False

        self_b = self.get_c()
        other_b = other.get_c()
        if self_b < other_b:
            return True
        if self_b > other_b:
            return False

        self_c = self.get_c()
        other_c = other.get_c()
        if self_c < other_c:
            return True
        if self_c > other_c:
            return False

        self_d = self.get_d()
        other_d = other.get_d()
        if self_d < other_d:
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
        self_a = self.get_a()
        other_a = other.get_a()
        if self_a < other_a:
            return True
        if self_a > other_a:
            return False

        self_b = self.get_b()
        other_b = other.get_b()
        if self_b < other_b:
            return True
        if self_b > other_b:
            return False

        self_c = self.get_c()
        other_c = other.get_c()
        if self_c < other_c:
            return True
        if self_c > other_c:
            return False

        self_d = self.get_d()
        other_d = other.get_d()
        if self_d <= other_d:
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
        self_a = self.get_a()
        other_a = other.get_a()
        if self_a > other_a:
            return True
        if self_a < other_a:
            return False

        self_b = self.get_c()
        other_b = other.get_c()
        if self_b > other_b:
            return True
        if self_b < other_b:
            return False

        self_c = self.get_c()
        other_c = other.get_c()
        if self_c > other_c:
            return True
        if self_c < other_c:
            return False

        self_d = self.get_d()
        other_d = other.get_d()
        if self_d > other_d:
            return True
        return False

    def __ge__(self, other):
        self_a = self.get_a()
        other_a = other.get_a()
        if self_a > other_a:
            return True
        if self_a < other_a:
            return False

        self_b = self.get_b()
        other_b = other.get_b()
        if self_b > other_b:
            return True
        if self_b < other_b:
            return False

        self_c = self.get_c()
        other_c = other.get_c()
        if self_c > other_c:
            return True
        if self_c < other_c:
            return False

        self_d = self.get_d()
        other_d = other.get_d()
        if self_d >= other_d:
            return True
        return False

    def __str__(self):
        a_val = self.get_a()
        b_val = self.get_b()
        c_val = self.get_c()
        d_val = self.get_d()
        if d_val != 0:
            string = "%d.%d.%d.%d" % (a_val, b_val, c_val, d_val)
        else:
            string = "%d.%d.%d" % (a_val, b_val, c_val)
        return string

    def step_major(self):
        """
        Increment the major part of the version number, the A in a.b.c.d.
        This clears (zeroes out) the other three fields.
        """
        a_val = self.get_a()
        a_val += 1
        if a_val > 255:
            raise RuntimeError("stepMajor() takes it out of range")
        else:
            self.value = DecimalVersion(a_val)

    def step_minor(self):
        """
        Increment the minor part of the version number, the B in a.b.c.d.
        This zeroes out the 'decimal' and 'micro' fields.
        """
        a_val = self.get_a()
        b_val = self.get_b()
        b_val += 1
        if b_val > 255:
            raise RuntimeError("stepMinor() takes it out of range")
        else:
            self.value = DecimalVersion(a_val, b_val)

    def step_decimal(self):
        """
        Increment the decimal part of the version number, the C in a.b.c.d.
        This clears the 4th 'micro' field.
        """
        a_val = self.get_a()
        b_val = self.get_b()
        c_val = self.get_c()
        c_val += 1
        if c_val > 255:
            raise RuntimeError("stepDecimal() takes it out of range")
        else:
            self.value = DecimalVersion(a_val, b_val, c_val)

    def step_micro(self):
        """
        Increment the micro part of the version number, the D in a.b.c.d.
        This leaves the other three fields unaffected.
        """
        a_val = self.get_a()
        b_val = self.get_b()
        c_val = self.get_c()
        d_val = self.get_d()
        d_val += 1
        if d_val > 255:
            raise RuntimeError("stepMicro() takes it out of range")
        else:
            self.value = DecimalVersion(a_val, b_val, c_val, d_val)

    # SYNONYMS ------------------------------------------------------
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

    def stepMajor(self):
        """ SYNONYM """
        self.step_major()

    def stepMinor(self):
        """ SYNONYM """
        self.step_minor()

    def stepDecimal(self):
        """ SYNONYM """
        self.step_decimal()

    def stepMicro(self):
        """ SYNONYM """
        self.step_micro()
    # END SYNONYMS --------------------------------------------------


def parse_decimal_version(string):
    """
    Expect the parameter s to be a string looking like a.b.c.d or a
    shorter version.  Returns a DecimalVersion object.
    """

    if string is None or string == "":
        raise RuntimeError("nil or empty version string")

    dver = None
    strings = string.split(".")
    length = len(strings)
    if length == 1:
        dver = DecimalVersion(strings[0])
    elif length == 2:
        dver = DecimalVersion(strings[0], strings[1])
    elif length == 3:
        dver = DecimalVersion(strings[0], strings[1], strings[2])
    elif length == 4:
        dver = DecimalVersion(strings[0], strings[1], strings[2], strings[3])
    else:
        raise RuntimeError("not a well-formed DecimalVersion: '%s'" % string)
    return dver

# TIMESTAMP FUNCTIONS -----------------------------------------------

# Note that in the Go code timestamp is an int64, whereas here it
# is a string.
# Note also that these functions will misbehave from 2038 or so.

# %T is shorthand for %H:%M:%S
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_timestamp(string):
    """
    If there is a decimal part to the seconds field, will raise ValueError
    with the message 'unconverted data remains: .123456'.
    """
    tstamp = time.strptime(string, TIMESTAMP_FORMAT)
    return calendar.timegm(tstamp)


def timestamp(nnn):       # sec from epoch
    """
    Given n the number of seconds from the epoch, return a string in
    the shorter format.  This truncates microseconds from the time.
    """
    tstamp = time.gmtime(nnn)
    return time.strftime(TIMESTAMP_FORMAT, tstamp)


def timestamp_now():
    """
    Get the current time, truncate it by omiting microseconds, and
    return a string in the shorter format.
    """
    tstamp = time.gmtime()
    return time.strftime(TIMESTAMP_FORMAT, tstamp)

# GLOBS, WILDCARDS --------------------------------------------------


def get_exclusions(proj_dir, excl_file='.gitignore'):
    """
    projDir must exist and may contain a .gitignore file containing one
    or more globs.

    Returns the contents of exclusion file (.girignore by default) as a
    list.  The list may be empty.  Any lines in the list are guaranteed
    be have had leading and trailing spaces stripped and will be
    non-empty.
    """

    globs = []
    path_to_ignore = os.path.join(proj_dir, excl_file)
    if os.path.isfile(path_to_ignore):
        with open(path_to_ignore, 'rb') as file:
            data = file.read().decode('utf8')
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
    regexes = regexes_from_wildcards(globs)
    return re.compile('|'.join(regexes))


def make_match_re(match_list):
    """
    Given a list of globs aka wildcards, return a compiled regular
    expression representing a match on one or more globs.  That is,
    we convert the wildcards to regular expressions, OR them all
    together, and compile and return the result.
    """
    return make_ex_re(match_list)


def regexes_from_wildcards(strings):
    """
    Given a list of wildcards, return a list of parenthesized
    regular expressions.
    """
    regexes = []
    if strings:
        for glob in strings:
            glob = glob.strip()
            # ignore empty wildcards
            if glob:
                # \Z means end of string, (?ms) means accept either
                # the M multiline flag or S, which makes . expand
                pat = fnmatch.translate(glob)
                regexes.append('(' + pat + ')')
    else:
        regexes.append('a^')      # matches nothing

    return regexes

# SYNONYMS ----------------------------------------------------------


def parseDecimalVersion(string):
    """ SYNONYM """
    return parse_decimal_version(string)


def parseTimestamp(string):
    """ SYNONYM """
    return parse_timestamp(string)


def timestampNow():
    """ SYNONYM """
    return timestamp_now()


def getExclusions(proj_dir, excl_file='.gitignore'):
    """ SYNONYM """
    return get_exclusions(proj_dir, excl_file)


def makeExRE(globs):
    """ SYNONYM """
    return make_ex_re(globs)


def makeMatchRE(match_list):
    """ SYNONYM """
    return make_match_re(match_list)


def regexesFromWildcards(strings):
    """ SYNONUM """
    return regexes_from_wildcards(strings)

# END SYNONYMS ------------------------------------------------------
