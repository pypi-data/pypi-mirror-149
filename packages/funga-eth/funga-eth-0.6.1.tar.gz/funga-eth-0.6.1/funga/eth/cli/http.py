# standard imports
import logging

# external imports
from http.server import (
        HTTPServer,
        BaseHTTPRequestHandler,
    )

# local imports
from .handle import SignRequestHandler
from funga.error import SignerError

logg = logging.getLogger(__name__)


def start_server_http(spec):
    httpd = HTTPServer(spec, HTTPSignRequestHandler)
    logg.debug('starting http server {}'.format(spec))
    httpd.serve_forever()


class HTTPSignRequestHandler(SignRequestHandler, BaseHTTPRequestHandler):

    def do_POST(self):
        if self.headers.get('Content-Type') != 'application/json':
            self.send_response(400, 'me read json only')
            self.end_headers()
            return

        try:
            if 'application/json' not in self.headers.get('Accept').split(','):
                self.send_response(400, 'me json only speak')
                self.end_headers()
                return
        except AttributeError:
            pass

        l = self.headers.get('Content-Length')
        try:
            l = int(l)
        except ValueError:
            self.send_response(400, 'content length must be integer')
            self.end_headers()
            return
        if l > 4096:
            self.send_response(400, 'too much information')
            self.end_headers()
            return
        if l < 0:
            self.send_response(400, 'you are too negative')
            self.end_headers()
            return

        b = b''
        c = 0
        while c < l:
            d = self.rfile.read(l-c)
            if d == None:
                break
            b += d
            c += len(d)
            if c > 4096:
                self.send_response(413, 'i should slap you around for lying about your size')
                self.end_headers()
                return

        try:
            r = self.handle_jsonrpc(d)
        except SignerError as e:
            r = e.to_jsonrpc()

        l = len(r)
        self.send_response(200, 'You are the Keymaster')
        self.send_header('Content-Length', str(l))
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        c = 0
        while c < l:
            n = self.wfile.write(r[c:])
            c += n


