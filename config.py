import sys

PyCasterAuth = "hackme"
PyCasterPort = 4446
PyCasterSSL = False
PyCasterSSLKey = None
PyCasterSSLCert = None
PyCasterMaxListeners = 32
PyCasterSendLogging = False
PyCasterLogFile="log/PyCasterServer.log"
ORIGIN="Access-Control-Allow-Origin: SAMEORIGIN"
pages = [
    '/',
    '/listeners',
    '/max-listeners',
    '/title',
    '/length',
    '/bitrate',
    '/img/background.jpg',
    '/img/content-bg.png'
]

