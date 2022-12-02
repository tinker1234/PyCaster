import config
import json
import PyCasterError
import socket
import mutagen
import os
import base64
import glob
import log
import time
import random
import ssl



class PyCaster:
    def __init__(self):
        self.ok = False
        self.id3 = {}
        self._listen = True
        try:
            if config.PyCasterSSL:
                ctx = ssl.create_default_context()
                with socket.create_connection(config.PyCasterHost, config.PyCasterPort) as sock:
                    with ctx.wrap_socket(sock, server_hostname=config.PyCasterHost) as self._socket:
                        pass
            else:
                self._socket = socket.socket()
                self._socket.connect((config.PyCasterHost, config.PyCasterPort))
        except Exception as e:
            raise PyCasterError.PyCasterConnect(e)
        self.init()

    def event(self, **kw):
        k = json.dumps(kw).encode()
        self._socket.send(k)

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
        self.id3['type'] = config.PyCasterContentType
        self.event(info=self.id3)
        log.log("Now Playing: " + title, 0)
        log.log(f"Loop: {config.loop}\nShuffle: {config.shuffle}", 0)
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
                    log.log(msg, 2)
                    raise PyCasterError.PyCasterInvalidAuth(msg)
                if login == "source-exists":
                    log.log(msg, 2)
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
        log.log(f"Using directory: {directory.replace(pattern, '')}  found {len(gl)} songs", 0)
        return gl
    
    def load_from_playlist(self, playlist = config.playlist):
        """
        @playlist: playlist file filled with songs 
        """
        songs = list()
        f = open(playlist, "r")
        for line in f.readlines():
            if len(line) != 0:
                line = line.strip()
                songs.append(line)
        f.close()
        if config.shuffle:
            random.shuffle(songs)
        log.log(f"Using playlist: {playlist} found {len(songs)} songs", 0)
        return songs


    def init(self):
        pass
