import socket
import ssl

class SSLSocket(object):
    def __init__(self, *args):
        self._socket = socket.socket(*args)
        self.SSLsocket = ssl.SSLSocket(self._socket)
    def socket(self): return self.SSLsocket