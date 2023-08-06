# standard imports
import re
import os
import sys
import json
import logging 
import argparse
from urllib.parse import urlparse

# external imports
import confini
from jsonrpc.exceptions import *

# local imports
from funga.eth.signer import EIP155Signer
from funga.eth.keystore.sql import SQLKeystore
from funga.eth.cli.handle import SignRequestHandler

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
config_dir = os.path.join(data_dir, 'config')

db = None
signer = None
session = None
chainId = 8995
socket_path = '/run/crypto-dev-signer/jsonrpc.ipc'


argparser = argparse.ArgumentParser()
argparser.add_argument('-c', type=str, default=config_dir, help='config file')
argparser.add_argument('--env-prefix', default=os.environ.get('CONFINI_ENV_PREFIX'), dest='env_prefix', type=str, help='environment prefix for variables to overwrite configuration')
argparser.add_argument('-i', type=int, help='default chain id for EIP155')
argparser.add_argument('-s', type=str, help='socket path')
argparser.add_argument('-v', action='store_true', help='be verbose')
argparser.add_argument('-vv', action='store_true', help='be more verbose')
args = argparser.parse_args()

if args.vv:
    logging.getLogger().setLevel(logging.DEBUG)
elif args.v:
    logging.getLogger().setLevel(logging.INFO)

config = confini.Config(args.c, args.env_prefix)
config.process()
config.censor('PASSWORD', 'DATABASE')
config.censor('SECRET', 'SIGNER')
logg.debug('config loaded from {}:\n{}'.format(config_dir, config))

if args.i:
    chainId = args.i
if args.s:
    socket_url = urlparse(args.s)
elif config.get('SIGNER_SOCKET_PATH'):
    socket_url = urlparse(config.get('SIGNER_SOCKET_PATH'))


# connect to database
dsn = 'postgresql://{}:{}@{}:{}/{}'.format(
        config.get('DATABASE_USER'),
        config.get('DATABASE_PASSWORD'),
        config.get('DATABASE_HOST'),
        config.get('DATABASE_PORT'),
        config.get('DATABASE_NAME'),    
    )

logg.info('using dsn {}'.format(dsn))
logg.info('using socket {}'.format(config.get('SIGNER_SOCKET_PATH')))

re_http = r'^http'
re_tcp = r'^tcp'
re_unix = r'^ipc'

class MissingSecretError(Exception):
    pass


def main():

    secret_hex = config.get('SIGNER_SECRET')
    if secret_hex == None:
        raise MissingSecretError('please provide a valid hex value for the SIGNER_SECRET configuration variable')

    secret = bytes.fromhex(secret_hex)
    kw = {
            'symmetric_key': secret,
            }
    SignRequestHandler.keystore = SQLKeystore(dsn, **kw)
    SignRequestHandler.signer = EIP155Signer(SignRequestHandler.keystore)

    arg = None
    try:
        arg = json.loads(sys.argv[1])
    except:
        logg.info('no json rpc command detected, starting socket server {}'.format(socket_url))
        scheme = 'ipc'
        if socket_url.scheme != '':
            scheme = socket_url.scheme
        if re.match(re_tcp, socket_url.scheme):
            from funga.eth.cli.socket import start_server_tcp
            socket_spec = socket_url.netloc.split(':')
            host = socket_spec[0]
            port = int(socket_spec[1])
            start_server_tcp((host, port))
        elif re.match(re_http, socket_url.scheme):
            from funga.eth.cli.http import start_server_http
            socket_spec = socket_url.netloc.split(':')
            host = socket_spec[0]
            port = int(socket_spec[1])
            start_server_http((host, port))
        else:
            from funga.eth.cli.socket import start_server_unix
            start_server_unix(socket_url.path)
        sys.exit(0)
   
    (rpc_id, response) = process_input(arg)
    r = jsonrpc_ok(rpc_id, response)
    sys.stdout.write(json.dumps(r))


if __name__ == '__main__':
    main()
