from twisted.python import log
from twisted.internet import reactor,ssl, protocol
import config
import uuid
import json
import header

class cl:
    clients = list()
    source = None
    sourceID = None
    sent_header = list()
    id3_headers = {
        "title": "None",
        "length": "0",
        "bitrate": "0"
    }

class RadioServer(protocol.Protocol):

    def connectionMade(self):
        if config.PyCasterMaxListeners != len(cl.clients):
            self.id = str(uuid.uuid4())
            self.peer = str(self.transport.getPeer())
            cl.clients.append(self)
            print("Client-Connected-IP: "+self.peer)
            print("Client-Connected-ID: " + self.id)
        else:
            self.transport.abortConnection()

    def connectionLost(self, reason):
        if self.id == cl.sourceID:
            print("Source-Closed: "+ str(reason))
            cl.sourceID = None
            cl.source = None
        else:
            self.removeClient(self.id)
            print("Client-Closed-Reason: " + str(reason))
            print("Client-Closed-IP: " + self.peer)
            print("Client-Closed-ID: " + self.id)

    def dataReceived(self, data):
        try: dct = json.loads(data)
        except: dct = {}
        if dct.has_key("PyCasterAuth"):
            if not cl.sourceID:
                auth = dct['PyCasterAuth']
                if auth == config.PyCasterAuth:
                    cl.source = self
                    cl.sourceID = self.id
                    self.transport.write("ok")
                    print("Source-Registered")
                    print("Source-ID: " + self.id)
                    self.removeClient(self.id)
                else:
                    cl.source.transport.write("denied")
                    print("Source-Login-Denied-IP: " + self.peer)
                    print("Source-Login-Denied-ID: " + self.id)
            else:
                print("Source-Exists-IP: " + self.peer)
                print("Source-Exists-ID: " + self.id)
                self.closeCl(self.id)

        elif dct.has_key("info"):
            cl.id3_headers = dct["info"]

        elif dct.has_key("buffer"):
            buffer = dct['buffer'].decode('base64')
            self.sendClients(buffer, bin=True)

    def removeClient(self, id):
        for client in cl.clients:
            if client.id == id:
                cl.clients.remove(client)
        for client in cl.sent_header:
            if client.id == id:
                cl.sent_header.remove(client)

    def closeCl(self, id):
        for client in cl.clients:
            if client.id == id:
                self.removeClient(id)
                client.transport.abortConnection()
                print("Server-Closed-Client: (%s, %s)" % (id, client.peer))


    def sendClients(self, msg, bin=False):
        for client in cl.clients:
            if client.id == cl.sourceID:
                self.removeClient(client.id)
            if bin:
                if client not in cl.sent_header:
                    head = header.header
                    head = head\
                        .replace("$title", cl.id3_headers['title'])\
                        .replace("$length", str(cl.id3_headers['length']))\
                        .replace("$listen", str(len(cl.clients)))\
                        .replace("$bitrate", str(cl.id3_headers['bitrate']))\
                        .replace("$max", str(config.PyCasterMaxListeners))
                    client.transport.write("HTTP/1.1 200 OK\r\n"+bytes(head))
                    cl.sent_header.append(client)
            client.transport.write(msg)
            if config.PyCasterSendLogging:
                print("SENT %i bytes TO %s" % (len(msg), client.id))


if __name__=="__main__":
    import sys
    key = config.PyCasterSSLKey
    cert = config.PyCasterSSLCert
    factory = protocol.Factory()
    log.startLogging(config.PyCasterLogFile)
    factory.protocol = RadioServer
    if config.PyCasterSSL:
        reactor.listenSSL(config.PyCasterPort, factory,  ssl.DefaultOpenSSLContextFactory(key, cert))
        reactor.run()
    else:
        reactor.listenTCP(config.PyCasterPort, factory)
        reactor.run()

