# standard imports
import logging
import binascii
import re

# external imports
#from rlp import encode as rlp_encode
from hexathon import (
        strip_0x,
        add_0x,
        int_to_minbytes,
        )

# local imports
from funga.eth.encoding import chain_id_to_v
#from funga.eth.rlp import rlp_encode
import rlp

logg = logging.getLogger(__name__)

rlp_encode = rlp.encode

class Transaction:
    
    def rlp_serialize(self):
        raise NotImplementedError

    def serialize(self):
        raise NotImplementedError


class EIP155Transaction:

    def __init__(self, tx, nonce_in, chainId_in=1):
        to = b''
        data = b''
        if tx.get('to') != None:
            to = bytes.fromhex(strip_0x(tx['to'], allow_empty=True))
        if tx.get('data') != None:
            data = bytes.fromhex(strip_0x(tx['data'], allow_empty=True))

        gas_price = None
        start_gas = None
        value = None
        nonce = None
        chainId = None

        # TODO: go directly from hex to bytes
        try:
            gas_price = int(tx['gasPrice'])
            byts = ((gas_price.bit_length()-1)/8)+1
            gas_price = gas_price.to_bytes(int(byts), 'big')
        except ValueError:
            gas_price = bytes.fromhex(strip_0x(tx['gasPrice'], allow_empty=True))

        try:
            start_gas = int(tx['gas'])
            byts = ((start_gas.bit_length()-1)/8)+1
            start_gas = start_gas.to_bytes(int(byts), 'big')
        except ValueError:
            start_gas = bytes.fromhex(strip_0x(tx['gas'], allow_empty=True))

        try:
            value = int(tx['value'])
            byts = ((value.bit_length()-1)/8)+1
            value = value.to_bytes(int(byts), 'big')
        except ValueError:
            value = bytes.fromhex(strip_0x(tx['value'], allow_empty=True))

        try:
            nonce = int(nonce_in)
            byts = ((nonce.bit_length()-1)/8)+1
            nonce = nonce.to_bytes(int(byts), 'big')
        except ValueError:
            nonce = bytes.fromhex(strip_0x(nonce_in, allow_empty=True))

        try:
            chainId = int(chainId_in)
            byts = ((chainId.bit_length()-1)/8)+1
            chainId = chainId.to_bytes(int(byts), 'big')
        except ValueError:
            chainId = bytes.fromhex(strip_0x(chainId_in, allow_empty=True))

        self.nonce = nonce
        self.gas_price = gas_price
        self.start_gas = start_gas
        self.to = to
        self.value = value
        self.data = data
        self.v = chainId
        self.r = b''
        self.s = b''
        self.sender = strip_0x(tx['from'])


    def canonical_order(self):
        s = [
            self.nonce,
            self.gas_price,
            self.start_gas,
            self.to,
            self.value,
            self.data,
            self.v,
            self.r,
            self.s,
                ]

        return s


    def bytes_serialize(self):
        s = self.canonical_order()
        b = b''
        for e in s:
            b += e
        return b
   

    def rlp_serialize(self):
        s = self.canonical_order()
        return rlp_encode(s)


    def serialize(self):
        tx = {
            'nonce': add_0x(self.nonce.hex(), allow_empty=True),
            'gasPrice': add_0x(self.gas_price.hex()),
            'gas': add_0x(self.start_gas.hex()),
            'value': add_0x(self.value.hex(), allow_empty=True),
            'data': add_0x(self.data.hex(), allow_empty=True),
            'v': add_0x(self.v.hex(), allow_empty=True),
            'r': add_0x(self.r.hex(), allow_empty=True),
            's': add_0x(self.s.hex(), allow_empty=True),
            }
        if self.to == None or len(self.to) == 0:
            tx['to'] = None
        else:
            tx['to'] = add_0x(self.to.hex())

        if tx['data'] == '':
            tx['data'] = '0x'

        if tx['value'] == '':
            tx['value'] = '0x00'

        if tx['nonce'] == '':
            tx['nonce'] = '0x00'

        return tx


    def apply_signature(self, chain_id, signature, v=None):
        if len(self.r + self.s) > 0:
            raise AttributeError('signature already set')
        if len(signature) < 65:
            raise ValueError('invalid signature length')
        if v == None:
            v = chain_id_to_v(chain_id, signature)
        self.v = int_to_minbytes(v)
        self.r = signature[:32]
        self.s = signature[32:64]
            
        for i in range(len(self.r)):
            if self.r[i] > 0:
                self.r = self.r[i:]
                break

        for i in range(len(self.s)):
            if self.s[i] > 0:
                self.s = self.s[i:]
                break
