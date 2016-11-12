# xlattice_py/xlattice/crypto.py

__all__ = ['AES_BLOCK_SIZE',
           'pkcs7_padding', 'add_pkcs7_padding', 'strip_pkcs7_padding',
           'next_nb_line', 'collect_pem_rsa_public_key',
           # Classes
           'SP',
           ]

# EXPORTED CONSTANTS

AES_BLOCK_SIZE = 16


class CryptoException(Exception):
    pass

# SYNONYMS used while refactoring dependent classes =================


def pkcs7Padding(data, block_size):
    """ SYNONYM """
    return pkcs7_padding(data, block_size)


def addPKCS7Padding(data, block_size):
    """ SYNONYM """
    return add_pkcs7_padding(data, block_size)


def stripPKCS7Padding(data, block_size):
    """ SYNONYM """
    return strip_pkcs7_padding(data, block_size)


def nextNBLine(strings):
    """ SYNONYM """
    return next_nb_line(strings)


def collectPEMRSAPublicKey(first_line, lines):
    """ SYNONYM """
    return collect_pem_rsa_public_key(first_line, lines)

# END SYN

# PKSC7 PADDING =====================================================


def pkcs7_padding(data, block_size):
    block_size = int(block_size)
    if block_size < 1:
        raise CryptoException("impossible block size")
    if not data:
        length = 0
    else:
        length = len(data)

    # we want from 1 to block_size bytes of padding
    n_blocks = int((length + block_size - 1) / block_size)
    rem = n_blocks * block_size - length
    if rem == 0:
        rem = block_size
    padding = bytearray(rem)    # that many null bytes
    for iii in range(rem):
        padding[iii] = rem      # padding bytes set to length of padding
    return padding


def add_pkcs7_padding(data, block_size):
    if block_size <= 1:
        raise CryptoException("impossible block size")
    else:
        padding = pkcs7_padding(data, block_size)
        if not data:
            out = padding
        else:
            out = data + padding
    return out


# The data passed is presumed to have PKCS7 padding.  If possible, return
# a copy of the data without the padding.  Return an error if the padding
# is incorrect.

def strip_pkcs7_padding(data, block_size):
    if block_size <= 1:
        raise CryptoException("impossible block size")
    elif not data:
        raise CryptoException("cannot strip padding from empty data")
    len_data = len(data)
    if len_data < block_size:
        raise CryptoException("data too short to have any padding")
    else:
        # examine the very last byte: it must be padding and must
        # contain the number of padding bytes added
        len_padding = data[len_data - 1]
        if len_padding < 1 or len_data < len_padding:
            raise CryptoException("incorrect PKCS7 padding")
        else:
            out = data[:len_data - len_padding]
    return out


# STRING ARRAYS / PEM SERIALIZSTION =================================

class SP(object):

    __SPACES__ = ['']

    @staticmethod
    def get_spaces(nnn):
        """ cache strings of N spaces """
        kkk = len(SP.__SPACES__) - 1
        while kkk < nnn:
            kkk = kkk + 1
            SP.__SPACES__.append(' ' * kkk)
        return SP.__SPACES__[nnn]

    @staticmethod
    def getSpaces(nnn):
        """ SYNONYM """

        return SP.get_spaces(nnn)


def next_nb_line(lines):
    """
    Enter with a reference to a list of lines.  Return the next line
    which is not empty after trimming, AND a reference to the edited
    array of strings.
    """
    if lines is not None:
        while len(lines) > 0:
            line = lines[0]
            lines = lines[1:]
            line = line.strip()
            if line != '':
                return line, lines
        raise RuntimeError("exhausted list of strings")
    raise RuntimeError("arg to nextNBLine cannot be None")


def collect_pem_rsa_public_key(first_line, lines):
    """
    Given the opening line of the PEM serializaton of an RSA Public Key,
    and a pointer to an array of strings which should begin with the rest
    of the PEM serialization, return the entire PEM serialization as a
    single string.
    """

    # XXX PROBLEM: PyCrypto omits "RSA ", pycryptodome doesn't.
    #   Including 'RSA ' appears to be correct.
    first_line = first_line.strip()
    if first_line != '-----BEGIN RSA PUBLIC KEY-----' and \
            first_line != '-----BEGIN PUBLIC KEY-----':
        raise RuntimeError('PEM public key cannot begin with %s' % first_line)
    found_last = False

    # DEBUG
    #ndx = 0
    #print("%2d %s" % (ndx, first_line))
    # END

    ret = [first_line]      # of string
    while len(lines) > 0:
        line, lines = next_nb_line(lines)
        # DEBUG
        #ndx += 1
        #print("%2d %s" % (ndx, line))
        # END
        ret = ret + [line]
        if line == '-----END RSA PUBLIC KEY-----' or  \
                line == '-----END PUBLIC KEY-----':
            found_last = True
            break

    if not found_last:
        raise RuntimeError("didn't find closing line of PEM serialization")
    return '\n'.join(ret), lines
