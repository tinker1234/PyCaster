# Latest Version Not Tested
    * dropped support for python 2.7.x
# PyCaster
PyCaster is a live radio streamer. You can stream MP3 files live to as many clients as possible, it uses twisted for most of the heavy stuff and is 100% open source.
server up at: [radio](http://otku.ga:4446/)

# What's new?
1. PyCaster server now contains a home page
2. When no source is connected it'll output a message saying so on `/<anything but resource>`
3. PyCaster index file contains variables
4. mountpoint added set in clients config file

# What's coming?

1. D.J client using wxpython
2. better documentation
3. an actual mini template for http side of server
\
# Server config.py

```python
PyCasterAuth = "hackme" # auth source will send
PyCasterPort = 4446 # server port
PyCasterSSL = False # use ssl/tls
PyCasterSSLKey = None # only need to worry about if PyCasterSSL is enabled
PyCasterSSLCert = None # only need to worry about if PyCasterSSL is enabled
PyCasterMaxListeners = 32 # max connections not including source
PyCasterSendLogging = False # log whats sent number of bytes and id/peer
PyCasterLogFile="log/PyCasterServer.log"
pages = [] # list of urls server will ignore sending buffer data to
```
# Client config.py
```python
PyCasterHost = "127.0.0.1" # host to connect to PyCaster server
PyCasterPort = 4446 # Port
PyCasterAuth = "hackme" # Password to connect to server to stream music
PyCasterSSL = False # Use SSL for HTTPS connections
playlist = None # Playlist file a new line per song
loop = False # loop directory or playlist
shuffle = False # Shuffle songs
directory = None # must be /path/to/songs/*.mp3
PyCasterMount = None #mount point default is /;
PyCasterLogFile="log/PyCaster.log" # log file location
PyCasterContentType="audio/mp3" # content type to send to server
```

# Special vars in index.html
`$host` replaced with server host
`$port` replaced with port set in server config
`$mount` replaced with mount client sends if no mount then anything is a mountpoint
`$type` replaced with content type sent by client (defaults to audio/mp3)

# How to run 
```bash
pip -r requirements.txt

python server.py
python client/PyCaster.py

``
