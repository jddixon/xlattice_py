# xlattice_py/xlattice/ui.py

import re
from distutils.util import strtobool

__all__ = ['confirm_y_or_n', 'passwd_strength', ]


def confirm_y_or_n(prompt, default='y'):
    """
    Prompt for agreement to continue.  Any default should be one of
    'y', 'n', 'yes', 'no', etc.
    """
    do_it = False
    prompt = "%s (default = '%s') " % (prompt, default)
    while True:
        reply = input(prompt)
        if reply == '':
            reply = default
        try:
            do_it = strtobool(reply)
            break
        except ValueError:
            print("please type 'y' or 'n'")
    return do_it


def passwd_strength(ppp):
    """
    Return a crude estimate of strength, a string.

    This should be improved by eg penalizing dictionary words
    and sequences of identical ('0000...') or ascending ('abc...")
    or descending ('zyxw...') characters.  This will be expensive
    but password changes should be infrequent.  The improved
    password strength estimator should then be moved into s
    separate package.
    """

    if not ppp:
        ppp = ''
    length = len(ppp)
    if length == 0:
        est = 'empty password'
    elif length < 6:
        est = 'too short'
    elif re.search(r'password', ppp, re.IGNORECASE):
        est = 'contains dictionary word'
    else:
        if length > 16:
            length = 16
        char_set_size = 0
        if re.search(r'[a-z]', ppp):
            char_set_size += 26
        if re.search(r'[A-Z]', ppp):
            char_set_size += 26
        if re.search(r'\d', ppp):
            char_set_size += 10
        if re.search(r'[^\w]', ppp):
            char_set_size += 16  # say ;-)

        if length >= 12:
            if char_set_size >= 52:
                est = 'very strong'
            else:
                est = 'strong'
        elif length >= 10:
            if char_set_size >= 52:
                est = 'strong'
            else:
                est = 'medium'
        elif length >= 8:
            if char_set_size >= 52:
                est = 'medium'
            else:
                est = 'fair'
        else:
            if char_set_size >= 78:
                est = 'fair'
            elif char_set_size >= 52:
                est = 'poor'
            else:
                est = 'weak'

        # DEBUG
        print(("length %d, charSetSize %d: %s" % (
            length, char_set_size, est)))
        # END

    return est
