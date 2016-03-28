# xlattice_py/xlattice/ui.py

import re
from distutils.util import strtobool

__all__ = ['confirmYorN', 'passwdStrength', ]


def confirmYorN(prompt, default='y'):
    """
    Prompt for agreement to continue.  Any default should be one of
    'y', 'n', 'yes', 'no', etc.
    """
    doIt = False
    prompt = "%s (default = '%s') " % (prompt, default)
    while True:
        reply = input(prompt)
        if reply == '':
            reply = default
        try:
            doIt = strtobool(reply)
            break
        except ValueError:
            print("please type 'y' or 'n'")
    return doIt


def passwdStrength(p):
    """
    Return a crude estimate of strength, a string.

    This should be improved by eg penalizing dictionary words
    and sequences of identical ('0000...') or ascending ('abc...")
    or descending ('zyxw...') characters.  This will be expensive
    but password changes should be infrequent.  The improved
    password strength estimator should then be moved into s
    separate package.
    """

    if not p:
        p = ''
    length = len(p)
    if length == 0:
        est = 'empty password'
    elif length < 6:
        est = 'too short'
    elif re.search(r'password', p, re.IGNORECASE):
        est = 'contains dictionary word'
    else:
        if length > 16:
            length = 16
        charSetSize = 0
        if re.search(r'[a-z]', p):
            charSetSize += 26
        if re.search(r'[A-Z]', p):
            charSetSize += 26
        if re.search(r'\d', p):
            charSetSize += 10
        if re.search(r'[^\w]', p):
            charSetSize += 16  # say ;-)

        if length >= 12:
            if charSetSize >= 52:
                est = 'very strong'
            else:
                est = 'strong'
        elif length >= 10:
            if charSetSize >= 52:
                est = 'strong'
            else:
                est = 'medium'
        elif length >= 8:
            if charSetSize >= 52:
                est = 'medium'
            else:
                est = 'fair'
        else:
            if charSetSize >= 78:
                est = 'fair'
            elif charSetSize >= 52:
                est = 'poor'
            else:
                est = 'weak'

        # DEBUG
        print(("length %d, charSetSize %d: %s" % (
            length, charSetSize, est)))
        # END

    return est
