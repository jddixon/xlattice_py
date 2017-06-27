# xlattice_py/xlattice/digsigner.py


"""
Digital signature generator.  Instances of this are created
by invoking Key.get_signer(digest_name).

@see Key
"""

from abc import ABCMeta, abstractmethod


class DigSigner(metaclass=ABCMeta):
    """ Digital signature generator. """

    @abstractmethod
    def get_algorithm(self):        # -> str
        """ Return the name of the algorithm used. """

    @abstractmethod
    def __len__(self):              # -> int
        """ Return the length of the digital signature generated. """

    @abstractmethod
    def update(self, data, offset, length):  # -> DigSigner, raises CryptoError
        """
        Add the binary data referenced to any already processed by
        the message digest part of the algorithm.
        """

    @abstractmethod
    def sign(self):     # -> byte[]             # raises CryptoError
        """
        Generate a digital signature and implicitly reset(self).

        Return the digital signature as a byte array.
        """
