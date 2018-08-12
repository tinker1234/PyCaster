import config
import json
import PyCasterError
import SSLSocket
import socket
import mutagen
import base64



class Pycaster:
    def __init__(self):
        self.ok = False
        self._listen = True
        try:
            if config.PyCasterSSL:
                self._socket = SSLSocket.SSLSocket().socket()
                self._socket.connect((config.PyCasterHost, config.PyCasterPort))
            else:
                self._socket = socket.socket()
                self._socket.connect((config.PyCasterHost, config.PyCasterPort))
        except Exception as e:
            raise PyCasterError.PyCasterConnect(e.message)

    def event(self, **kw):
        k = json.dumps(kw)
        self._ws.send(k)

    def login_as_source(self):
        if not config.PyCasterMount:
            self.event(PyCasterAuth=config.PyCasterAuth)
        else:
            self.event(PyCasterAuth=config.PyCasterAuth, PyCasterMount=config.PyCasterMount)

    def send(self, buffer):
        if self.ok: 
            self.event(buffer=base64.b64encode(buffer))

    def file(self, file):
        f =open(file, "rb")
        mp3 = mutagen.File(file)
        try:
            title = mp3['title']
        except:
            title = f.name.split(os.sep)[-1].replace(".mp3", "").replace(".ogg", "")

        self.id3['title'] = title
        self.id3['bitrate'] = mp3.info.bitrate
        self.id3['length'] = mp3.info.length
        self.id3['stream-start'] = time.time() * 1000
        self.event(info=self.id3)
        log.log("Now Playing: " + title, 0)
        log.log("Loop: %s\nShuffle: %s" % (config.loop, config.shuffle), 0)
        return f

    def loopme(self):
        if self.ok:
            self.setListen(0)
        if self._listen:
            data = str(self._socket.recv(1024))
            try: js = json.loads(data)
            except: js = {}
            if "login" in js:
                login = js['login']
                msg = js['message']
                if login == "OK":
                    self.ok = True
                    log.log("OK", 0)
                if login == "denied":
                    log.log(msg, 0)
                    raise PyCasterError.PyCasterInvalidAuth(msg)
                if login == "source-exists":
                    log.log(msg, 0)
                    raise PyCasterError.PyCasterAlreadyLoggedIn(msg)



    def setListen(self, bolean):
        if bolean:
            self._listen = True
        if not bolean:
            self._listen = False

    def load_from_dir(self, directory = config.directory, pattern = "*.mp3"):
        """
        @directory: directory where the songs are
        @pattern: regex pattern to grab songs from directory
        """
        if directory[-1] == os.sep: directory = directory + pattern
        else: directory = directory + os.sep + pattern
        gl = glob.glob(directory)
        if config.shuffle:
            random.shuffle(gl)
        log.log("Using directory: %s found %i songs" % (directory.replace(pattern, ""), len(gl)), 0)
        return gl