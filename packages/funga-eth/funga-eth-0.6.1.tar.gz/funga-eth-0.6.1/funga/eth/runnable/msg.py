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
from funga.eth.keystore.dict import DictKeystore
from funga.eth.signer import EIP155Signer


logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

argparser = argparse.ArgumentParser()
argparser.add_argument('-f', type=str, help='Keyfile to use for signing')
argparser.add_argument('-z', action='store_true', help='zero-length password')
argparser.add_argument('-v', action='store_true', help='be verbose')
argparser.add_argument('-0', dest='nonl', action='store_true', help='no newline at end of output')
argparser.add_argument('msg', type=str, help='Message to sign')
args = argparser.parse_args()

if args.v:
    logg.setLevel(logging.DEBUG)


def main():
    passphrase = os.environ.get('WALLET_PASSPHRASE', os.environ.get('PASSPHRASE'))
    if args.z:
        passphrase = ''
    if passphrase == None:
        passphrase = getpass.getpass('decryption phrase: ')
   
    keystore = DictKeystore()
    address = keystore.import_keystore_file(args.f, password=passphrase)

    signer = EIP155Signer(keystore)
    sig = signer.sign_ethereum_message(address, args.msg.encode('utf-8').hex(), password=passphrase)

    r = sig.hex()
    if not args.nonl:
        r += "\n"
    sys.stdout.write(r)


if __name__ == '__main__':
    main()
