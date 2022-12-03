# Latest Version Not Tested

# config
```python
PyCasterHost = "127.0.0.1" # server host
PyCasterPort = 4446 # server port
PyCasterAuth = "123abc" # auth to be sent to the server
PyCasterSSL = False # connect via https
PyCasterMount = None # mount sent to the server
playlist = None # playlist of set mp3s
loop = False # never end stream, if false the client wil close after all files have been played
shuffle = False # shuffle the songs, this shuffles everytime getSongs is called
directory = None # this gets loaded into glob so directory path has to include regex
# directory = "music/*.mp3"
PyCasterContentType="audio/mp3" # content type to send to server
PyCasterLogFile = "log/PyCaster.log
```

# file method
file methed handles openning the mp3 and getting id3 tags.
It returns a file object

# login_as_source method
Sends the auth to the server
Sends mount to server

# errors
```
PyCasterConnect: raised when can't connect to the server.
PyCasterConnectionLost: raised when server closes the conection or goes down.
PyCasterInvalidAuth: raised if the auth sent to the server is wrong.
PyCasterAlreadyLoggedIn: raised if a source is already connected to the server.
```
# how to run
```bash
python PyCaster.py
```
