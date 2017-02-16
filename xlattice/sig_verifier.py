# xlattice_py/xlattice/sig_verifier.py

"""
Given a PublicKey, instances of this class can verify digital
signatures.
"""

from abc import ABCMeta, abstractmethod


class SigVerifier(metaclass=ABCMeta):
    """
    Given a PublicKey, instances of this class can verify digital
    signatures.
    """

    @property
    @abstractmethod
    def algorithm(self):        # -> str
        """ Return the name of the algorithm. """

    @abstractmethod
    def __init__(self, pubkey):
        """
        Initialize the verifier for use with a particular PublicKey.

        @param pubkey PublicKey against which digital signature is verified
        """

    @abstractmethod
    def update(self, data, offset, length):   # -> SigVerifier
        """
        Add block of data to that being checked.

        @param data byte array being added
        Return     reference to this verifier as a convenience in chaining
        """

    @abstractmethod
    def verify(self, dig_sig, offset, length):   # -> bool
        """
        Check the digital signature passed against the data accumulated.

        @param dig_sig signature being checked
        Return       whether the check is successful
        """
