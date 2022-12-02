import time
import PyCasterClient
import config


class PyCaster(PyCasterClient.PyCaster):
    def init(self):
        self.login_as_source()
        self.count = -1


    def getSongs(self):
        if config.directory: return self.load_directory()
        elif config.playlist: return self.load_playlist()

    def load_directory(self, directory=None, pattern=None):
        """
        if all values are None it sets values from config.py
        """
        if directory and pattern:
            songs = self.load_from_dir(directory=directory, pattern=pattern)
        elif directory:
            songs = self.load_from_dir(directory=directory)
        elif pattern:
            songs = self.load_from_dir(pattern=pattern)
        else:
            songs = self.load_from_dir()
        return songs

    def load_playlist(self, playlist = None):
        """
        if all values are None it sets values from config.py
        """
        if playlist:
            return self.load_from_playlist(playlist=playlist)
        else:
            return self.load_from_playlist()

    def _next(self):
        songs = self.getSongs()
        if config.loop:
            if len(songs) >= self.count + 1:
                self.count = 0
            else:
                self.count += 1
        else:
            self.count += 1 # error will stop loop
        self.main()


    def main(self):
        song = self.file(self.getSongs()[self.count])
        buf = song.read(4096)
        while True:
            nbuf = buf
            buf = song.read(4096)
            self.loopme()
            if len(nbuf) == 0:
                break
            self.send(nbuf)
            time.sleep(0.1)

        self._next()

if __name__=="__main__":
    pyc = PyCaster()
    pyc.main()
