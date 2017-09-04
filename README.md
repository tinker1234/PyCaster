# PyCaster
PyCaster is a live radio streamer. You can stream MP3 files live to as many clients as possible, it uses twisted for most of the heavy stuff and is 100% open source.
server up at: [radio](https://otku.ga:4446/)

# Server.py

```python
# connectionMade
    def connectionMade(self):
        if config.PyCasterMaxListeners != len(cl.clients):
            self.id = str(uuid.uuid4()) # assigns a unique id to every client that connects
            self.peer = str(self.transport.getPeer())
            cl.clients.append(self)
            print("Client-Connected-IP: "+self.peer)
            print("Client-Connected-ID: " + self.id)
        else:
            self.transport.abortConnection() # close and remove from connection pool

# connectionLost
 def connectionLost(self, reason):
        if self.id == cl.sourceID: # we check if its the source
            print("Source-Closed: "+ str(reason))
            # reset its id and connection
            cl.sourceID = None 
            cl.source = None
        else:
          #if not source then kill the client
            self.removeClient(self.id)
            print("Client-Closed-Reason: " + str(reason))
            print("Client-Closed-IP: " + self.peer)
            print("Client-Closed-ID: " + self.id)
`
# sending to clients
def sendClients(self, msg, bin=False):
        for client in cl.clients: # itrate through each client
            if client.id == cl.sourceID: # make sure we dont echo back to our source
                self.removeClient(client.id)
            if bin: # if buffer data
                if client not in cl.sent_header: # check so we dont keep resending headers causing glitches in audio
                    head = header.header
                    head = head\
                         # I figured replace would be better then iteration
                        .replace("$title", cl.id3_headers['title'])\
                        .replace("$length", str(cl.id3_headers['length']))\
                        .replace("$listen", str(len(cl.clients)))\
                        .replace("$max", str(config.PyCasterMaxListeners))
                    client.transport.write("HTTP/1.1 200 OK\r\n"+bytes(head))
                    cl.sent_header.append(client) # put client in here so it wont resend
            client.transport.write(msg)
            if config.PyCasterSendLogging:
                print("SENT %i bytes TO %s" % (len(msg), client.id))

# closing clients
    def closeCl(self, id):
        for client in cl.clients: # we iterate over the clients to find the matching id
            if client.id == id:
                self.removeClient(id) # remove from sent_headers and clients
                client.transport.abortConnection() # completely kill the client connection
                print("Server-Closed-Client: (%s, %s)" % (id, client.peer))
```

# config.py

```python
PyCasterAuth = "123abc" # auth source will send
PyCasterPort = 4446 # server port
PyCasterSSL = False # use ssl/tls
PyCasterSSLKey = None # only need to worry about if PyCasterSSL is enabled
PyCasterSSLCert = None # only need to worry about if PyCasterSSL is enabled
PyCasterMaxListeners = 32 # max connections not including source
PyCasterSendLogging = False # log whats sent number of bytes and id/peer
PyCasterLogFile=open("pycaster.log", "w") # can be sys.stdout
```
# How to run 
```bash
pip -r requirements.txt
python server.py
``
