# standard imports
import json
import logging

# external imports
from jsonrpc.exceptions import (
        JSONRPCServerError,
        JSONRPCParseError,
        JSONRPCInvalidParams,
        )
from hexathon import add_0x

# local imports
from funga.eth.transaction import EIP155Transaction
from funga.error import (
        UnknownAccountError,
        SignerError,
        )
from funga.eth.cli.jsonrpc import jsonrpc_ok
from .jsonrpc import (
        jsonrpc_error,
        is_valid_json,
        )

logg = logging.getLogger(__name__)


class SignRequestHandler:

    keystore = None
    signer = None

    def process_input(self, j):
        rpc_id = j['id']
        m = j['method']
        p = j['params']
        return (rpc_id, getattr(self, m)(p))


    def handle_jsonrpc(self, d):
        j = None
        try:
            j = json.loads(d)
            is_valid_json(j)
            logg.debug('{}'.format(d.decode('utf-8')))
        except Exception as e:
            logg.exception('input error {}'.format(e))
            j = json.dumps(jsonrpc_error(None, JSONRPCParseError)).encode('utf-8')
            raise SignerError(j)

        try:
            (rpc_id, r) = self.process_input(j)
            r = jsonrpc_ok(rpc_id, r)
            j = json.dumps(r).encode('utf-8')
        except ValueError as e:
            # TODO: handle cases to give better error context to caller
            logg.exception('process error {}'.format(e))
            j = json.dumps(jsonrpc_error(j['id'], JSONRPCServerError)).encode('utf-8')
            raise SignerError(j)
        except UnknownAccountError as e:
            logg.exception('process unknown account error {}'.format(e))
            j = json.dumps(jsonrpc_error(j['id'], JSONRPCServerError)).encode('utf-8')
            raise SignerError(j)

        return j


    def personal_newAccount(self, p):
        password = p
        if p.__class__.__name__ != 'str':
            if p.__class__.__name__ != 'list':
                e = JSONRPCInvalidParams()
                e.data = 'parameter must be list containing one string'
                raise ValueError(e)
            logg.error('foo {}'.format(p))
            if len(p) != 1:
                e = JSONRPCInvalidParams()
                e.data = 'parameter must be list containing one string'
                raise ValueError(e)
            if p[0].__class__.__name__ != 'str':
                e = JSONRPCInvalidParams()
                e.data = 'parameter must be list containing one string'
                raise ValueError(e)
            password = p[0]

        r = self.keystore.new(password)
                 
        return add_0x(r)


    # TODO: move to translation module ("personal" rpc namespace is node-specific)
    def personal_signTransaction(self, p):
        logg.debug('got {} to sign'.format(p[0]))
        t = EIP155Transaction(p[0], p[0]['nonce'], p[0]['chainId'])
        raw_signed_tx = self.signer.sign_transaction_to_rlp(t, p[1])
        o = {
            'raw': '0x' + raw_signed_tx.hex(),
            'tx': t.serialize(),
            }
        return o


    def eth_signTransaction(self, tx):
        o = self.personal_signTransaction([tx[0], ''])
        return o['raw']


    def eth_sign(self, p):
        logg.debug('got message {} to sign'.format(p[1]))
        message_type = type(p[1]).__name__
        if message_type != 'str':
            raise ValueError('invalid message format, must be {}, not {}'.format(message_type))
        z = self.signer.sign_ethereum_message(p[0], p[1][2:])
        return add_0x(z.hex())

