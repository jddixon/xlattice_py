# ~/dev/py/xlattice_py/xlattice/node.py

"""
XLattice Node core functionality.

This code will only be used temporarily, while AbstractNode, BaseNode, etc
are being sorted out.
"""

from abc import ABCMeta
import os
import sys
import hashlib

from Crypto.PublicKey import RSA as rsa

from xlattice import HashTypes, check_hashtype  # , UnrecognizedSHAError

if sys.version_info < (3, 6):
    # pylint: disable=unused-import
    import sha3
    assert sha3     # suppress warning:w


class BaseNode(ABCMeta):
    """
    Parent class for Node-like things.
    """

    def __init__(self, hashtype=HashTypes.SHA2, sk_pub=None, ck_pub=None,
                 node_id=None):

        check_hashtype(hashtype)
        self._hashtype = hashtype
        if node_id is None:
            if ck_pub:

                # we have called checkUsingSHA(): one of these cases must apply
                if hashtype == HashTypes.SHA1:
                    sha = hashlib.sha1()
                elif hashtype == HashTypes.SHA2:
                    sha = hashlib.sha256()
                elif hashtype == HashTypes.SHA3:
                    sha = hashlib.sha3_256
                sha.update(ck_pub.exportKey())
                node_id = sha.digest()    # a binary value
            else:
                raise ValueError('cannot calculate nodeID without pubKey')

        self._node_id = node_id
        self._sk_pub = sk_pub
        self._ck_pub = ck_pub

    @property
    def node_id(self):
        """ Return the 160- or 256-bit node ID. """
        return self._node_id

    @property
    def sk_pub(self):
        """ Return the public part of the Node's RSA key for signing. """
        return self._sk_pub

    @property
    def ck_pub(self):
        """ Return the public part of the Node's RSA key for encryption. """
        return self._ck_pub


class Node(BaseNode):
    """
    The cryptographic identity of an XLattice Node: its nodeID and RSA keys.
    """

    def __init__(self, hashtype=HashTypes.SHA2, sk_priv=None, ck_priv=None):

        # making this the default value doesn't work: it always
        # generates the same key
        if sk_priv is None:
            sk_priv = rsa.generate(2048, os.urandom)
        node_id, ck_pub = Node.calc_id_and_ck_pub_for_node(
            hashtype, sk_priv)
        BaseNode.__init__(self, hashtype, ck_pub, node_id)

        if not sk_priv:
            raise ValueError('INTERNAL ERROR: undefined private key')
        self._sk_priv = sk_priv

        # each of these needs some sort of map or maps, or we will have to do
        # a linear search
        self._peers = []
        self._overlays = []    #
        self._connections = []    # with peers? with clients?

    def create_from_key(self, string):
        """
        Given the serialization of a node, create one.


        Despite the name, this should also handle peer lists, etc.

        XXX WE ALSO NEED a serialization function
        """
        pass

    @staticmethod
    def calc_id_and_ck_pub_for_node(hashtype, rsa_sk_priv):
        """ Calculate a NodeID and public key, given an RSA private key. """
        check_hashtype(hashtype)
        (node_id, ck_pub) = (None, None)
        ck_pub = rsa_sk_priv.publickey()

#       # DEBUG
#       print "GET_ID: private key is %s" % str(rsaPrivateKey.__class__)
#       print "    has_private = %s" % rsaPrivateKey.has_private()
#       print "GET_ID: public key is  %s" % str(pubKey.__class__)
#       print "    has_private = %s" % pubKey.has_private()
#       # END

        # generate the nodeID from the public key
        if hashtype == HashTypes.SHA1:
            sha = hashlib.sha1()
        elif hashtype == HashTypes.SHA2:
            sha = hashlib.sha256()
        elif hashtype == HashTypes.SHA3:
            sha = hashlib.sha3_256()

        sha.update(ck_pub.exportKey())
        node_id = sha.digest()
        return (node_id,                 # nodeID = 160/256 bit BINARY value
                ck_pub)                 # from private key

    @property
    def skey(self):
        """ Return this node's RSA private key for signing. """
        return self._sk_priv

    @property
    def ckey(self):
        """ Return this node's RSA private key for encryption. """
        return self._sk_priv

    # these work with
    def sign(self, msg):
        """ Sign a message using this node's private key. """
        sha = hashlib.sha1()
        sha.update(bytes(msg))
        d_val = sha.digest()
        return self._sk_priv.sign(d_val, msg)

    def verify(self, msg, signature):
        """ Verify the digital signature using this node's private key. """
        sha = hashlib.sha1()
        sha.update(bytes(msg))
        d_val = sha.digest()
        return self._ck_pub.verify(d_val, signature)


class Peer(BaseNode):
    """ a Peer is a Node seen from the outside """

    def __init__(self, hashtype=HashTypes.SHA2, node_id=None,
                 ck_pub=None, sk_pub=None):
        BaseNode.__init__(self, hashtype, node_id, sk_pub, ck_pub)
