from twisted.internet import reactor, ssl, protocol
import config
import uuid
import json
import header
import re
import log
import base64

def get(data):
    pattern = b"GET (/.*?)\s+HTTP"
    m=re.search(pattern, data)
    if m: return m.group(1).decode()


class cl:
    clients = list()
    source = None
    sourceID = None
    sent_header = list()
    id3_headers = {
        "title": "None",
        "length": "0",
        "bitrate": "0",
        "type": "audio/mp3"
    }

class RadioServer(protocol.Protocol):
    mount = None

    def connectionMade(self):
        if config.PyCasterMaxListeners != len(cl.clients):
            self.id = str(uuid.uuid4())
            self.peer = str(self.transport.getPeer())
            log.log(f"Client-Connected-IP: {self.peer}")
            log.log(f"Client-Connected-ID: {self.id}")
        else:
            self.transport.abortConnection()
            log.log("Client-Limit")

    def connectionLost(self, reason):
        if self.id == cl.sourceID:
            log.log(f"Source-Closed: {str(reason)}")
            cl.sourceID = None
            cl.source = None
        else:
            self.removeClient(self.id)
            log.log(f"Client-Closed-Reason: {str(reason)}")
            log.log(f"Client-Closed-IP: {self.peer}")
            log.log(f"Client-Closed-ID: {self.id}")

    def dataReceived(self, data):
        try: dct = json.loads(data)
        except: dct = {}

        if not self.mount:
            content = "<b>Source not connected</b>"
            self.HTTPSendClient(f"HTTP 200 OK\r\n{header.HTTP_RESP.format('text/html', len(content), content)}")
        elif get(data) == "/":
            mount = ";"
            if self.mount:
                mount = self.mount
            with open("index.html", "r") as content:
                content = content.read()
                content = content.replace("$host", self.transport.getHost().host).replace("$port", str(config.PyCasterPort)).replace("$mount", mount)
                resp = f"HTTP/1.1 200 OK\r\n{config.ORIGIN}\r\n{header.HTTP_RESP.format('text/html', len(content), content)}"
                log.log(f"Client-Http-GET: {get(data)}")
                self.HTTPSendClient(resp)

        elif get(data) == "/img/background.jpg":
            with open("img/background.jpg", "rb") as content:
                content = content.read()
                resp = f"HTTP/1.1 200 OK\r\n{config.ORIGIN}\r\n{header.IMAGE_RESP.format('image/jpg', len(content))}"
                log.log(f"Client-Http-GET: {get(data)}")
                self.HTTPSendClient(resp)
                self.HTTPSendClient(content, bin=True)

        elif get(data) == "/img/content-bg.png":
            with open("img/content-bg.png", "rb") as content:
                content = content.read()
                resp = f"HTTP/1.1 200 OK\r\n{config.ORIGIN}\r\n{header.IMAGE_RESP.format('image/png', len(content))}"
                log.log(f"Client-Http-GET: {get(data)}")
                self.HTTPSendClient(resp)
                self.HTTPSendClient(content, bin=True)

        elif get(data) == "/title":
            resp = f"HTTP/1.1 200 OK\r\n{config.ORIGIN}\r\n{header.HTTP_RESP.format('text/plain', len(cl.id3_headers['title']), cl.id3_headers['title'])}"
            log.log(f"Client-Http-GET: {get(data)}")
            self.HTTPSendClient(resp)

        elif get(data) == "/listeners":
            resp = f"HTTP/1.1 200 OK\r\n{config.ORIGIN}\r\n{header.HTTP_RESP.format('text/plain', len(cl.clients), len(cl.clients))}"
            log.log(f"Client-Http-GET: {get(data)}")
            self.HTTPSendClient(resp)

        elif get(data) == "/max-listeners":
            resp = f"HTTP/1.1 200 OK\r\n{header.HTTP_RESP.format('text/plain', len(str(config.PyCasterMaxListeners)), config.PyCasterMaxListeners)}"
            log.log(f"Client-Http-GET: {get(data)}")
            self.HTTPSendClient(resp)

        elif get(data) == "/bitrate":
            resp = f"HTTP/1.1 200 OK\r\n{header.HTTP_RESP.format('text/plain', len(str(cl.id3_headers['bitrate'])), cl.id3_headers['bitrate'])}"
            log.log(f"Client-Http-GET: {get(data)}")
            self.HTTPSendClient(resp)

        elif get(data) == "/length":
            resp = f"HTTP/1.1 200 OK\r\n{header.HTTP_RESP.format('text/plain', len(str(cl.id3_headers['length'])), cl.id3_headers['length'])}"
            log.log(f"Client-Http-GET: {get(data)}")
            self.HTTPSendClient(resp)

        elif "PyCasterAuth" in dct:
            if not cl.sourceID:
                auth = dct['PyCasterAuth']
                if auth == config.PyCasterAuth:
                    cl.source = self
                    cl.sourceID = self.id
                    event = {"login": "OK", "message": "None"}
                    self.sendEvent(**event)
                    log.log("Source-Registered")
                    log.log(f"Source-ID: {self.id}")
                else:

                    event = {"login": "denied", "message": "Invalid auth"}
                    self.sendEvent(**event)
                    log.log(f"Source-Login-Denied-IP: {self.peer}")
                    log.log(f"Source-Login-Denied-ID: {self.id}")

            else:
                log.log(f"Source-Exists-IP: {self.peer}")
                log.log(f"Source-Exists-ID: {self.id}")
                event = {"login": "denied", "message": "Source exists"}
                self.sendEvent(**event)
                self.closeCl(self.id)
    
        elif "PyCasterMount" in dct:
            self.mount = dct['PyCasterMount']

        elif "info" in dct:
            cl.id3_headers = dct["info"]

        elif "buffer" in dct:
            buffer = base64.b64decode(dct['buffer'])
            self.sendClients(buffer)
        
        elif get(data) not in config.pages:
            content = "Not Found(404)"
            self.HTTPSendClient(f"HTTP 200 OK\r\n{header.HTTP_RESP.format('text/html', len(content), content)}")

        elif get(data) == self.mount:
            cl.clients.append(self)

    def removeClient(self, id):
        found = None
        for client in cl.clients:
            if client.id == id:
                found = client
                if client in cl.sent_header:
                    cl.sent_header.remove(client)
        if found: cl.clients.remove(found)

    def sendEvent(self, **event):
        event = json.dumps(event).encode()
        self.transport.write(event)

    def closeCl(self, id):
        for client in cl.clients:
            if client.id == id:
                self.removeClient(id)
                client.transport.abortConnection()
                log.log(f"Server-Closed-Client: ({id}, {client.peer})")


    def HTTPSendClient(self, msg, bin=False):
        log.log(f"Client-Http-Resp-ID: {self.id}")
        log.log(f"Client-Http-Resp-IP: {self.peer}")
        if bin: self.transport.write(msg)
        else: self.transport.write(msg.encode())


    def sendClients(self, msg):
        for client in cl.clients:
            if client.id == cl.sourceID:
                self.removeClient(client.id)
            if client not in cl.sent_header:
                head = header.header
                head = head\
                    .replace("$title", cl.id3_headers['title'])\
                    .replace("$length", str(cl.id3_headers['length']))\
                    .replace("$listen", str(len(cl.clients)))\
                    .replace("$bitrate", str(cl.id3_headers['bitrate']))\
                    .replace("$max", str(config.PyCasterMaxListeners))\
                    .replace("$type", cl.id3_headers['type'])
                client.transport.write(f"HTTP/1.1 200 OK\r\n{head}".encode())
                cl.sent_header.append(client)
            client.transport.write(msg)
            if config.PyCasterSendLogging:
                log.log(f"SENT {len(msg)} bytes TO {client.id}")


if __name__=="__main__":
    key = config.PyCasterSSLKey
    cert = config.PyCasterSSLCert
    factory = protocol.Factory()
    factory.protocol = RadioServer
    if config.PyCasterSSL:
        reactor.listenSSL(config.PyCasterPort, factory,  ssl.DefaultOpenSSLContextFactory(key, cert))
        reactor.run()
    else:
        reactor.listenTCP(config.PyCasterPort, factory)
        reactor.run()

