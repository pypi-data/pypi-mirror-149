# standard imports
import os
import logging 
import socket
import stat

# local imports
from funga.error import SignerError
from .handle import SignRequestHandler

logg = logging.getLogger(__name__)


class SocketHandler:

    def __init__(self):
        self.handler = SignRequestHandler()


    def process(self, csock):
        d = csock.recv(4096)
       
        r = None
        try:
            r = self.handler.handle_jsonrpc(d)
        except SignerError as e:
            r = e.to_jsonrpc()

        csock.send(r)


def start_server_socket(s):
    s.listen(10)
    logg.debug('server started')
    handler = SocketHandler()
    while True:
        (csock, caddr) = s.accept()
        handler.process(csock)
        csock.close()
    s.close()
    os.unlink(socket_path)


def start_server_tcp(spec):
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(spec)
    logg.debug('created tcp socket {}'.format(spec))
    start_server_socket(s)


def start_server_unix(socket_path):
    socket_dir = os.path.dirname(socket_path)
    try:
        fi = os.stat(socket_dir)
        if not stat.S_ISDIR:
            RuntimeError('socket path {} is not a directory'.format(socket_dir))
    except FileNotFoundError:
        os.mkdir(socket_dir)

    try:
        os.unlink(socket_path)
    except FileNotFoundError:
        pass
    s = socket.socket(family = socket.AF_UNIX, type = socket.SOCK_STREAM)
    s.bind(socket_path)
    logg.debug('created unix ipc socket {}'.format(socket_path))
    start_server_socket(s)
