# xlattice_py/xlattice/secret.py

""" A secret, a symmetric cryptographic key. """

from abc import ABCMeta, abstractmethod


class Secret(metaclass=ABCMeta):
    """ A secret, a symmetric cryptographic key. """

    @property
    @abstractmethod
    def algorithm(self):    # -> str
        """ Return the name of the algorithm, for example, "aes". """
