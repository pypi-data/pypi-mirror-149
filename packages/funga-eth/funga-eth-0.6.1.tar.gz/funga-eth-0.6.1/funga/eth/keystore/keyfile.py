# standard imports
import os
import hashlib
import logging
import json
import uuid

# external imports
import coincurve
from Crypto.Cipher import AES
from Crypto.Util import Counter
import sha3

# local imports
from funga.error import (
    DecryptError,
    KeyfileError,
)
from funga.eth.encoding import private_key_to_address

logg = logging.getLogger(__name__)

algo_keywords = [
    'aes-128-ctr',
]
hash_keywords = [
    'scrypt',
    'pbkdf2'
]

default_scrypt_kdfparams = {
    'dklen': 32,
    'n': 1 << 18,
    'p': 1,
    'r': 8,
    'salt': os.urandom(32).hex(),
}

default_pbkdf2_kdfparams = {
    'c': 100000,
    'dklen': 32,
    'prf': 'sha256',
    'salt': os.urandom(32).hex(),
}

def to_mac(mac_key, ciphertext_bytes):
    h = sha3.keccak_256()
    h.update(mac_key)
    h.update(ciphertext_bytes)
    return h.digest()


class Hashes:

    @staticmethod
    def from_scrypt(kdfparams=default_scrypt_kdfparams, passphrase=''):
        dklen = int(kdfparams['dklen'])
        n = int(kdfparams['n'])
        p = int(kdfparams['p'])
        r = int(kdfparams['r'])
        salt = bytes.fromhex(kdfparams['salt'])

        return hashlib.scrypt(passphrase.encode('utf-8'), salt=salt, n=n, p=p, r=r, maxmem=1024 * 1024 * 1024,
                              dklen=dklen)

    @staticmethod
    def from_pbkdf2(kdfparams=default_pbkdf2_kdfparams, passphrase=''):
        if kdfparams['prf'] == 'hmac-sha256':
            kdfparams['prf'].replace('hmac-sha256','sha256')

        derived_key = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=passphrase.encode('utf-8'),
            salt=bytes.fromhex(kdfparams['salt']),
            iterations=int(kdfparams['c']),
            dklen=int(kdfparams['dklen'])
        )
        return derived_key


class Ciphers:
    aes_128_block_size = 1 << 7
    aes_iv_len = 16

    @staticmethod
    def decrypt_aes_128_ctr(ciphertext, decryption_key, iv):
        ctr = Counter.new(Ciphers.aes_128_block_size, initial_value=iv)
        cipher = AES.new(decryption_key, AES.MODE_CTR, counter=ctr)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext

    @staticmethod
    def encrypt_aes_128_ctr(plaintext, encryption_key, iv):
        ctr = Counter.new(Ciphers.aes_128_block_size, initial_value=iv)
        cipher = AES.new(encryption_key, AES.MODE_CTR, counter=ctr)
        ciphertext = cipher.encrypt(plaintext)
        return ciphertext


def to_dict(private_key_bytes, kdf='scrypt', passphrase=''):
    private_key = coincurve.PrivateKey(secret=private_key_bytes)

    if kdf == 'scrypt':
        encryption_key = Hashes.from_scrypt(passphrase=passphrase)
        kdfparams = default_scrypt_kdfparams

    elif kdf == 'pbkdf2':
        encryption_key = Hashes.from_pbkdf2(passphrase=passphrase)
        kdfparams = pbkdf2_kdfparams

    else:
        raise NotImplementedError("KDF not implemented: {0}".format(kdf))

    address_hex = private_key_to_address(private_key)
    iv_bytes = os.urandom(Ciphers.aes_iv_len)
    iv = int.from_bytes(iv_bytes, 'big')
    ciphertext_bytes = Ciphers.encrypt_aes_128_ctr(private_key.secret, encryption_key[:16], iv)

    mac = to_mac(encryption_key[16:], ciphertext_bytes)

    crypto_dict = {
        'cipher': 'aes-128-ctr',
        'ciphertext': ciphertext_bytes.hex(),
        'cipherparams': {
            'iv': iv_bytes.hex(),
        },
        'kdf': kdf,
        'kdfparams': kdfparams,
        'mac': mac.hex(),
    }

    uu = uuid.uuid1()
    o = {
        'address': address_hex,
        'version': 3,
        'crypto': crypto_dict,
        'id': str(uu),
    }
    return o


def from_dict(o, passphrase=''):
    cipher = o['crypto']['cipher']
    if cipher not in algo_keywords:
        raise NotImplementedError('cipher "{}" not implemented'.format(cipher))

    kdf = o['crypto']['kdf']
    if kdf not in hash_keywords:
        raise NotImplementedError('kdf "{}" not implemented'.format(kdf))

    m = getattr(Hashes, 'from_{}'.format(kdf.replace('-', '_')))
    decryption_key = m(o['crypto']['kdfparams'], passphrase)

    control_mac = bytes.fromhex(o['crypto']['mac'])
    iv_bytes = bytes.fromhex(o['crypto']['cipherparams']['iv'])
    iv = int.from_bytes(iv_bytes, "big")
    ciphertext_bytes = bytes.fromhex(o['crypto']['ciphertext'])

    # check mac
    calculated_mac = to_mac(decryption_key[16:], ciphertext_bytes)
    if control_mac != calculated_mac:
        raise DecryptError('mac mismatch when decrypting passphrase')

    m = getattr(Ciphers, 'decrypt_{}'.format(cipher.replace('-', '_')))

    try:
        pk = m(ciphertext_bytes, decryption_key[:16], iv)
    except AssertionError as e:
        raise DecryptError('could not decrypt keyfile: {}'.format(e))

    return pk


def from_file(filepath, passphrase=''):
    f = open(filepath, 'r')
    try:
        o = json.load(f)
    except json.decoder.JSONDecodeError as e:
        f.close()
        raise KeyfileError(e)
    f.close()

    return from_dict(o, passphrase)


def from_some(v, passphrase=''):
    if isinstance(v, bytes):
        v = v.decode('utf-8')

    if isinstance(v, str):
        try:
            return from_file(v, passphrase)
        except Exception:
            logg.debug('keyfile parse as file fail')
            pass
        v = json.loads(v)

    return from_dict(v, passphrase)
