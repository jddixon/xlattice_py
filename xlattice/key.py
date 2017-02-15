# xlattice_py/xlattice/key.py


"""
An asymmetric cryptographic key.

This will contain the information necessary to use the key with the
particular algorithm.
"""

from abc import ABCMeta, abstractmethod


class Key(metaclass=ABCMeta):
    """ An asymmetric cryptographic key. """

    @property
    @abstractmethod
    def algorithm(self):    # -> str
        """Return the name of the algorithm, for example, "rsa". """

    @abstractmethod
    def get_signer(self, digest_name):    # -> DigSigner, raises CryptoError
        """
        Given a message digest algorithm, return a reference to a
        digital signature generator suitable for this key.

        XXX This is an experiment - it might be considered a failure,
        XXX in that many public key cryptography algorithms are not
        XXX used for digital signatures.

        @param digestName case-insensitive name of the signature generator
        """

    @abstractmethod
    def get_public_key(self):   # -> PublicKey
        """
        Another experiment.
        """
