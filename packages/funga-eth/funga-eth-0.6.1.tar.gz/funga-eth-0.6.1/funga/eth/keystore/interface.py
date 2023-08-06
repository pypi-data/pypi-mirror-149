# standard imports
import os
import json
import logging

# local imports
from funga.eth.keystore import keyfile
from funga.eth.encoding import private_key_from_bytes
from funga.keystore import Keystore

logg = logging.getLogger(__name__)


def native_keygen(*args, **kwargs):
    return os.urandom(32)


class EthKeystore(Keystore):

    def __init__(self, private_key_generator=native_keygen):
        super(EthKeystore, self).__init__(private_key_generator, private_key_from_bytes, keyfile.from_some)
            

    def new(self, password=None):
        b = self.private_key_generator()
        return self.import_raw_key(b, password=password)


    def import_raw_key(self, b, password=None):
        pk = private_key_from_bytes(b)
        return self.import_key(pk, password)


    def import_key(self, pk, password=None):
        raise NotImplementedError


    def import_keystore_data(self, keystore_content, password=''):
        if type(keystore_content).__name__ == 'str':
            keystore_content = json.loads(keystore_content)
        elif type(keystore_content).__name__ == 'bytes':
            logg.debug('bytes {}'.format(keystore_content))
            keystore_content = json.loads(keystore_content.decode('utf-8'))
        private_key = keyfile.from_dict(keystore_content, password.encode('utf-8'))
        return self.import_raw_key(private_key, password)


    def import_keystore_file(self, keystore_file, password=''):
        private_key = keyfile.from_file(keystore_file, password)
        return self.import_raw_key(private_key)
