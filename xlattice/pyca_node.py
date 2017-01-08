# ~/dev/py/xlattice_py/xlattice/pyca_node.py

########################################
# BEING HACKED TO USED pyca/cryptography
########################################

import os
import sys

# from Crypto.PublicKey import RSA as rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

from xlattice import QQQ, check_using_sha  # , UnrecognizedSHAError


class AbstractNode(object):

    def __init__(self, using_sha=False, pub_key=None, node_id=None):

        check_using_sha(using_sha)
        self._using_sha = using_sha
        if node_id is None:
            if pub_key:
                # DEBUG
                print("AbstractNode: public key is %s" % str(pub_key))
                print("              class is %s" % pub_key.__class__)
                # END

                # we have called checkUsingSHA(): one of these cases must apply
                # pylint:disable=redefined-variable-type
                if using_sha == QQQ.USING_SHA1:
                    sha_ = hashes.SHA1
                elif using_sha == QQQ.USING_SHA2:
                    sha_ = hashes.SHA256
                sha = hashes.Hash(sha_(), backend=default.backend())
                # ----------------> XXXXXXXX
                sha.update(pub_key.exportKey())
                node_id = sha.digest()    # a binary value
            else:
                raise ValueError('cannot calculate nodeID without pubKey')

        self._node_id = node_id
        self._pub_key = pub_key

    @property
    def node_id(self):
        return self._node_id

    @property
    def pub_key(self):
        return self._pub_key


class Node(AbstractNode):
    """
    """

    def __init__(self, using_sha=QQQ.USING_SHA2, priv_key=None):

        # making this the default value doesn't work: it always
        # generates the same key
        if priv_key is None:
            # XXX SHOULD BE CREATING TWO PRIVATE KEYS
            priv_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,  # cheap key for testing
                backend=default_backend())
        node_id, pub_key = Node.get_id_and_pub_key_for_node(
            using_sha, self, priv_key)
        AbstractNode.__init__(self, using_sha, pub_key, node_id)

        if not priv_key:
            raise ValueError('INTERNAL ERROR: undefined private key')
        self._private_key = priv_key

        # each of these needs some sort of map or maps, or we will have to do
        # a linear search
        self._peers = []
        self._overlays = []    #
        self._connections = []    # with peers? with clients?

    def create_from_key(self, string):
        # XXX STUB: given the serialization of a node, create one
        # despite the name, this should also handle peer lists, etc
        # XXX WE ALSO NEED a serialization function
        pass

    @staticmethod
    def get_id_and_pub_key_for_node(using_sha, node, rsa_priv_key):

        check_using_sha(using_sha)
        (node_id, pub_key) = (None, None)
        pub_key = rsa_priv_key.public_key()
        pem_pub_key = pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.PKCS1)

#       # DEBUG
#       print "GET_ID: private key is %s" % str(rsaPrivateKey.__class__)
#       print "    has_private = %s" % rsaPrivateKey.has_private()
#       print "GET_ID: public key is  %s" % str(pubKey.__class__)
#       print "    has_private = %s" % pubKey.has_private()
#       # END

        # generate the nodeID from the public key
        # pylint: disable=redefined-variable-type
        if using_sha == QQQ.USING_SHA1:
            sha_ = hashes.SHA1
        elif using_sha == QQQ.USING_SHA2:
            sha_ = hashes.SHA256
        sha = hashes.Hash(sha_(), backend=default_backend())
        sha.update(pem_pub_key)
        node_id = sha.finalize()
        return (node_id,                 # nodeID = 160/256 bit BINARY value
                pub_key)                 # from private key

    @property
    def key(self):
        return self._private_key

    # these work with
    def sign(self, msg):
        sha = hashes.Hash(SHA1(), backend=default_backend())
        sha.update(bytes(msg))
        d_val = sha.digest()
        return self._private_key.sign(d_val, msg)

    def verify(self, msg, signature):
        sha = hashes.Hash(SHA1(), backend=default_backend())
        sha.update(bytes(msg))
        d_val = sha.digest()
        return self._pub_key.verify(d_val, signature)


class Peer(AbstractNode):
    """ a Peer is a Node seen from the outside """

    def __init__(self, using_sha=False, node_id=None, pub_key=None):
        AbstractNode.__init__(self, using_sha, node_id, pub_key)
