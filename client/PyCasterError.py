class PyCasterConnect(Exception):
    message = "Failed to connect to PyCaster.."
    def __init__(self, message=None):
        if message != None:
            self.message = message
        super(PyCasterConnect, self).__init__(self.message)

class PyCasterConnectionLost(Exception):
    message = "PyCaster connection lost.."
    def __init__(self, message=None):
        if message != None:
            self.message = message
        super(PyCasterConnectionLost, self).__init__(self.message)
class PyCasterInvalidAuth(Exception):
    message  = "Failed to authenticate with PyCaster.."
    def __init__(self, message=None):
        if message != None:
            self.message = message
        super(PyCasterInvalidAuth, self).__init__(self.message)

class PyCasterAlreadyLoggedIn(Exception):
    message = "A source is already logged in."
    def __init__(self, message=None):
        if message != None:
            self.message = message
        super(PyCasterAlreadyLoggedIn, self).__init__(self.message)
