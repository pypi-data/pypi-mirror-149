# standard imports
import logging

# external imports
import sha3
import coincurve
from hexathon import int_to_minbytes

# local imports
from funga.signer import Signer
from funga.eth.encoding import chain_id_to_v

logg = logging.getLogger(__name__)


class EIP155Signer(Signer):

    def __init__(self, keyGetter):
        super(EIP155Signer, self).__init__(keyGetter)


    def sign_transaction(self, tx, password=None):
        s = tx.rlp_serialize()
        h = sha3.keccak_256()
        h.update(s)
        message_to_sign = h.digest()
        z = self.sign_pure(tx.sender, message_to_sign, password)

        return z


    def sign_transaction_to_rlp(self, tx, password=None):
        chain_id = int.from_bytes(tx.v, byteorder='big')
        sig = self.sign_transaction(tx, password)
        tx.apply_signature(chain_id, sig)
        return tx.rlp_serialize()


    def sign_transaction_to_wire(self, tx, password=None):
        return self.sign_transaction_to_rlp(tx, password=password)


    def sign_ethereum_message(self, address, message, password=None):
        
        #k = keys.PrivateKey(self.keyGetter.get(address, password))
        #z = keys.ecdsa_sign(message_hash=g, private_key=k)
        if type(message).__name__ == 'str':
            logg.debug('signing message in "str" format: {}'.format(message))
            #z = k.sign_msg(bytes.fromhex(message))
            message = bytes.fromhex(message)
        elif type(message).__name__ == 'bytes':
            logg.debug('signing message in "bytes" format: {}'.format(message.hex()))
            #z = k.sign_msg(message)
        else:
            logg.debug('unhandled format {}'.format(type(message).__name__))
            raise ValueError('message must be type str or bytes, received {}'.format(type(message).__name__))

        ethereumed_message_header = b'\x19' + 'Ethereum Signed Message:\n{}'.format(len(message)).encode('utf-8')
        h = sha3.keccak_256()
        h.update(ethereumed_message_header + message)
        message_to_sign = h.digest()

        z = self.sign_pure(address, message_to_sign, password)
        return z


    # TODO: generic sign should be moved to non-eth context
    def sign_pure(self, address, message, password=None):
        pk = coincurve.PrivateKey(secret=self.keyGetter.get(address, password))
        z = pk.sign_recoverable(hasher=None, message=message)
        return z


    def sign_message(self, address, message, password=None, dialect='eth'):
        if dialect == None:
            return self.sign_pure(address, message, password=password)
        elif dialect == 'eth':
            return self.sign_ethereum_message(address, message, password=password)
        raise ValueError('Unknown message sign dialect "{}"'.format(dialect))
