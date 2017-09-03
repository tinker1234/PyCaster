import glob
import random
import time
import log
import PyCasterClient
import config


class PyCaster:
    def __init__(self):
        self._client = PyCasterClient.Pycaster()
        self._client.login_as_source()
        self.count = 3

    def getSongs(self):
        if config.directory:
            print(log.log("Using directory: "+ config.directory))
            songs = glob.glob(config.directory)
            if config.shuffle:
                random.shuffle(songs)
            print(log.log("Directory-Shuffle: %s,  with %i songs" % (config.shuffle, len(songs))))
            return songs

        elif config.playlist:
            try:
                print(log.log("Using playlist: " + config.playlist))
                songs = list()
                f = open(config.playlist, "r")
                for entry in f.readlines():
                    songs.append(entry.strip())
                f.close()
                if config.shuffle:
                    random.shuffle(songs)
                print(log.log("Playlist-Shuffle: %s,  with %i songs" % (config.shuffle, len(songs))))
                return songs
            except:
                print(log.log("Playlist not found", "err"))
                raise Exception(config.playlist + ' not found..')


    def _next(self):
        songs = self.getSongs()
        if config.loop:
            if len(songs) >= self.count+1:
                self.count = 0
            else:
                self.count += 1
            self.mainLoop()
        else:
            self.count += 1 # error will stop loop
            self.mainLoop()

    def mainLoop(self):
        song = self._client.file(self.getSongs()[self.count])
        print(log.log("Currently Playing: (" + song.name + ") with loop %s" % config.loop))
        buf = song.read(4096)
        while True:
            nbuf = buf
            buf = song.read(4096)
            self._client.loopme()
            if len(nbuf) == 0:
                log.log(song.name + " has ended")
                break
            self._client.send(nbuf)
            time.sleep(0.1)
        self._next()

if __name__=="__main__":
    pyc = PyCaster()
    pyc.mainLoop()