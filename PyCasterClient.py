import config
import json
import PyCasterError
import SSLSocket
import socket
import mutagen

class Pycaster:
    def __init__(self):
        self.ok = False
        self._info = {}
        self._has_sent = 0
        try:
            if config.PyCasterSSL:
                self._socket = SSLSocket.SSLSocket().socket()
                self._socket.connect((config.PyCasterHost, config.PyCasterPort))
            else:
                self._socket = socket.socket()
                self._socket.connect((config.PyCasterHost, config.PyCasterPort))
        except Exception as e:
            raise PyCasterError.PyCasterConnect(e.message)

    def file(self, file):
        _file = open(file, "rb")
        mp3 = mutagen.File(file)
        try:
            title = mp3['title']
        except:
            title = "None"
        dct = {
            'info': {
                "title": title,
                "length": mp3.info.length,
                "bitrate": mp3.info.bitrate
            }
        }
        self._has_sent = 0
        self._info = dct
        return _file


    def send(self, data, buffer=True):
        if self.ok:
            if not self._has_sent:
                self._socket.send(json.dumps(self._info))
                self._has_sent = 1
            if buffer: data = json.dumps({"buffer": data.encode('base64')})
            try:
                self._socket.send(data)
            except:
                raise PyCasterError.PyCasterConnectionLost

    def events(self, **kw):
        return json.dumps(kw)

    def _messageEvent(self, data):
        if data == "ok":
            self.ok = True
        elif data == "source-exists":
            raise PyCasterError.PyCasterAlreadyLoggedIn
        elif data == "denied":
            raise PyCasterError.PyCasterInvalidAuth

    def login_as_source(self):
        data = self.events(PyCasterAuth=config.PyCasterAuth, PyCasterMount=config.PyCasterMount)
        self._socket.send(data)

    def loopme(self):
        if not self.ok:
            try: self._messageEvent(self._socket.recv(13))
            except:
                raise PyCasterError.PyCasterConnectionLost