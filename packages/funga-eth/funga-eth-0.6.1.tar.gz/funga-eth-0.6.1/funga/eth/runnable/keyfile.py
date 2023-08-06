# standard imports
import os
import logging
import sys
import json
import argparse
import getpass

# external impors
import coincurve
from hexathon import strip_0x

# local imports
from funga.error import DecryptError
from funga.eth.keystore.keyfile import (
        from_file,
        to_dict,
        )


from funga.eth.encoding import (
        private_key_to_address,
        private_key_from_bytes,
        )


logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

argparser = argparse.ArgumentParser()
argparser.add_argument('-d', '--decrypt', dest='d', type=str, help='decrypt file')
argparser.add_argument('--private-key', dest='private_key', action='store_true', help='output private key instead of address')
argparser.add_argument('-0', dest='nonl', action='store_true', help='no newline at end of output')
argparser.add_argument('-z', action='store_true', help='zero-length password')
argparser.add_argument('-k', type=str, help='load key from file')
argparser.add_argument('-v', action='store_true', help='be verbose')
args = argparser.parse_args()

if args.v:
    logg.setLevel(logging.DEBUG)

mode = 'create'
secret = False
if args.d:
    mode = 'decrypt'
    if args.private_key:
        secret = True

pk_hex = os.environ.get('PRIVATE_KEY')
if args.k != None:
    f = open(args.k, 'r')
    pk_hex = f.read(66)
    f.close()

def main():
    global pk_hex

    passphrase = os.environ.get('WALLET_PASSPHRASE', os.environ.get('PASSPHRASE'))
    if args.z:
        passphrase = ''
    r = None
    if mode == 'decrypt':
        if passphrase == None:
            passphrase = getpass.getpass('decryption phrase: ')
        try:
            r = from_file(args.d, passphrase).hex()
        except DecryptError:
            sys.stderr.write('Invalid passphrase\n')
            sys.exit(1)
        if not secret:
            pk = private_key_from_bytes(bytes.fromhex(r))
            r = private_key_to_address(pk)
    elif mode == 'create':
        if passphrase == None:
            passphrase = getpass.getpass('encryption phrase: ')
        pk_bytes = None
        if pk_hex != None:
            pk_hex = strip_0x(pk_hex)
            pk_bytes = bytes.fromhex(pk_hex)
        else:
            pk_bytes = os.urandom(32)
        pk = coincurve.PrivateKey(secret=pk_bytes)
        o = to_dict(pk_bytes, passphrase=passphrase)
        r = json.dumps(o)

    if not args.nonl:
        r += "\n"
    sys.stdout.write(r) 


if __name__ == '__main__':
    main()
