header = "Transfer-Encoding: chuncked\r\nContent-Type: $type\r\nPyc-Title: $title\r\nPyc-Length: $length\r\nPyc-Bitrate: $bitrate\r\nPyc-Listeners: $listen\r\nPyc-Max-Listeners: $max\r\n\r\n"
HTTP_RESP = "Content-Type: {0}\r\nContent-Length: {1}\r\n\r\n{2}"
IMAGE_RESP = "Content-Type: {0}\r\nContent-Length: {1}\r\n\r\n"