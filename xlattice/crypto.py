# xlattice_py/xlattice/crypto.py

__all__ = [ 'AES_BLOCK_SIZE',
            'pkcs7Padding', 'addPKCS7Padding', 'stripPKCS7Padding',
            'nextNBLine',  'collectPEMRSAPublicKey',
            # Classes
            'SP',
          ]

# EXPORTED CONSTANTS

AES_BLOCK_SIZE  = 16


class CryptoException(Exception):
    pass

def pkcs7Padding(data, blockSize):
    blockSize = int(blockSize)
    if blockSize < 1:
        raise CryptoException("impossible block size")
    if not data:
        length = 0
    else:
        length = len(data)

    # we want from 1 to blockSize bytes of padding
    nBlocks = int((length + blockSize - 1) / blockSize)
    rem = nBlocks * blockSize - length
    if rem == 0:
        rem = blockSize
    padding = bytearray(rem)    # that many null bytes
    for i in range(rem):
        padding[i] = rem        # padding bytes set to length of padding
    return padding

# PKSC7 PADDING =====================================================

def addPKCS7Padding(data, blockSize):
    if blockSize <= 1 :
        raise CryptoException("impossible block size")
    else :
        padding = pkcs7Padding(data, blockSize)
        if not data :
            out = padding
        else :
            out = data + padding
    return out


# The data passed is presumed to have PKCS7 padding.  If possible, return
# a copy of the data without the padding.  Return an error if the padding
# is incorrect.

def stripPKCS7Padding(data, blockSize):
    if blockSize <= 1 :
        raise CryptoException("impossible block size")
    elif not data:
        raise CryptoException("cannot strip padding from empty data")
    lenData = len(data)
    if lenData < blockSize :
        raise CryptoException("data too short to have any padding")
    else :
        # examine the very last byte: it must be padding and must
        # contain the number of padding bytes added
        lenPadding = data[lenData-1]
        if lenPadding < 1 or lenData < lenPadding :
            raise CryptoException("incorrect PKCS7 padding")
        else :
            out = data[:lenData-lenPadding]
    return out


# STRING ARRAYS / PEM SERIALIZSTION =================================

class SP(object):

    __SPACES__ = ['']
    @staticmethod
    def getSpaces(n):
        """ cache strings of N spaces """
        k = len(SP.__SPACES__) - 1
        while k < n:
            k = k + 1
            SP.__SPACES__.append( ' ' * k) 
        return SP.__SPACES__[n] 

def nextNBLine(ss):
    """ 
    Enter with a reference to a list of lines.  Return the next line
    which is not empty after trimming, advancing the reference to the
    array of strings accordingly.
    """
    if ss != None:
        while len(ss) > 0:
            s  = ss[0]
            ss = ss[1:]
            s = s.strip()
            if s != '':
                return s, ss
        raise RuntimeError("exhausted list of strings")
    raise RuntimeError("arg to nextNBLine cannot be None")

def collectPEMRSAPublicKey(firstLine, ss):
    """
    Given the opening line of the PEM serializaton of an RSA Public Key, 
    and a pointer to an array of strings which should begin with the rest
    of the PEM serialization, return the entire PEM serialization as a 
    single string.  
    """

    firstLine = firstLine.strip()
    if firstLine != '-----BEGIN RSA PUBLIC KEY-----': 
        raise RuntimeError('PEM public key cannot begin with %s' % firstLine)
    foundLast = False

    # DEBUG
    #ndx = 0
    #print("%2d %s" % (ndx, firstLine))
    # END

    x = [firstLine]      # of string
    while len(ss) > 0:
        s, ss = nextNBLine(ss)
        # DEBUG
        #ndx += 1
        #print("%2d %s" % (ndx, s))
        # END
        x = x + [s]
        if s == '-----END RSA PUBLIC KEY-----' :
            foundLast = True
            break
    
    if not foundLast:
        raise RuntimeError ("didn't find closing line of PEM serialization")
    return '\n'.join(x), ss

