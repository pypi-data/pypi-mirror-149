# standard imports
import logging

# external imports
import coincurve
import sha3
from hexathon import (
        strip_0x,
        uniform,
        )

logg = logging.getLogger(__name__)


def private_key_from_bytes(b):
    return coincurve.PrivateKey(secret=b)


def public_key_bytes_to_address(pubk_bytes, result_format='hex'):
    h = sha3.keccak_256()
    logg.debug('public key bytes {}'.format(pubk_bytes.hex()))
    h.update(pubk_bytes[1:])
    z = h.digest()[12:]
    if result_format == 'hex':
        return to_checksum_address(z[:20].hex())
    elif result_format == 'bytes':
        return z[:20]
    raise ValueError('invalid result format "{}"'.format(result_format))


def public_key_to_address(pubk, result_format='hex'):
    pubk_bytes = pubk.format(compressed=False)
    return public_key_bytes_to_address(pubk_bytes, result_format='hex')


def private_key_to_address(pk, result_format='hex'):
    pubk = coincurve.PublicKey.from_secret(pk.secret)
    #logg.debug('secret {} '.format(pk.secret.hex()))
    return public_key_to_address(pubk, result_format)


def is_address(address_hex):
    try:
        address_hex = strip_0x(address_hex, pad=False)
    except ValueError:
        return False
    return len(address_hex) == 40


def is_checksum_address(address_hex):
    hx = None
    try:
        hx = to_checksum(address_hex)
    except ValueError:
        return False
    return hx == strip_0x(address_hex)


def to_checksum_address(address_hex):
        address_hex = strip_0x(address_hex, pad=False)
        if len(address_hex) != 40:
            raise ValueError('Invalid address length')
        address_hex = uniform(address_hex)
        h = sha3.keccak_256()
        h.update(address_hex.encode('utf-8'))
        z = h.digest()

        #checksum_address_hex = '0x'
        checksum_address_hex = ''

        for (i, c) in enumerate(address_hex):
            if c in '1234567890':
                checksum_address_hex += c
            elif c in 'abcdef':
                if z[int(i / 2)] & (0x80 >> ((i % 2) * 4)) > 1:
                    checksum_address_hex += c.upper()
                else:
                    checksum_address_hex += c

        return checksum_address_hex

to_checksum = to_checksum_address

ethereum_recid_modifier = 35

def chain_id_to_v(chain_id, signature):
    v = signature[64]
    return (chain_id * 2) + ethereum_recid_modifier + v

def chainv_to_v(chain_id, v):
    return v - ethereum_recid_modifier - (chain_id * 2)
