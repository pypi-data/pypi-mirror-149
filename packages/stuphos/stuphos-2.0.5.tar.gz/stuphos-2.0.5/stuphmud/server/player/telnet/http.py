# Telnet Dispatch Module.
from http.server import BaseHTTPRequestHandler
from io import StringIO as new_buffer

class TelnetHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request_message, peer, dispatch_module):
        self.request_message = request_message
        self.peer = peer
        self.dispatch_module = dispatch_module
        BaseHTTPRequestHandler.__init__(self, request_message, peer, dispatch_module)

    def setup(self):
        # Make request message readable by parse_request.
        self.rfile = self.request_message
        self.wfile = self.peer.response = new_buffer()

    def finish(self):
        # Do whatever it is the dispatch does with a response...
        #    A) put it on a response queue associated with peer?
        #    B) write it back to the peer via IAC?
        ##    if not self.wfile.closed:
        ##        self.wfile.flush()
        ##    self.wfile.close()
        ##    self.rfile.close()
        pass

def _doHttpRequest(peer, request_message):
    TelnetHTTPRequestHandler(request_message, peer, __import__(__name__, fromlist = ['']))
    # peer.response

def getDispatchAction(name):
    return (name == 'request') and _doHttpRequest

# Unit Testing.
from io import StringIO

class PeerHandle(StringIO):
    pass
class RequestMessage(StringIO):
    pass

REQUEST_MESSAGE = \
'''
'''

def getTelnetRequestComponents():
    peerHandle = PeerHandle()
    requestMessage = RequestMessage(REQUEST_MESSAGE)
    dispatchModule = __import__(__name__, fromlist = [''])

    return (requestMessage, peerHandle, dispatchModule)

def makeTelnetRequestHandler():
    (peerHandle, requestMessage, dispatchModule) = getTelnetRequestComponents()
    return TelnetHTTPRequestHandler(requestMessage, peerHandle, dispatchModule)

def simple_test(argv = None):
    (peerHandle, requestMessage, dispatchModule) = getTelnetRequestComponents()

    from pdb import runcall as run
    print(run(_doHttpRequest, peerHandle, requestMessage))

# A more complete server for configuring a fuller simple_test.
class THRHWrapper(BaseHTTPRequestHandler):
    # Simple _doHttpRequest, but from an actual live server.
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.telnetRequest = makeTelnetRequestHandler()
    def __repr__(self):
        return '{thrhWrapper: handling}'
    __str__ = __repr__

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", 'text/html')
        self.end_headers()

        print(generatePageResponse(self), file=self.wfile)

def generatePageResponse(self):
    this = __import__(__name__)
    # this = reload(this)
    return '<html><body>%s</body></html>' % this.generateBody(self)

def generateBody(self):
    return '%s\n%s\n' % (self, dir(self))

from http.server import HTTPServer
from _thread import start_new_thread as nth

class ServerControl:
    def is_running(self):
        return bool(getattr(self, '__running', False))
    def set_running(self, state):
        setattr(self, '__running', bool(state))

    def start(self):
        self.set_running(True)
        nth(self.serve_forever, ())
        return self
    def stop(self):
        self.set_running(False)
        self.server_close()

    def serve_forever(self):
        while self.is_running():
            self.handle_request()

class TestServer(HTTPServer, ServerControl):
    PORT = 8181
    def __init__(self):
        HTTPServer.__init__(self, ('localhost', self.PORT), THRHWrapper)
    def __repr__(self):
        return '{testServer: booted}'
    __str__ = __repr__

def server_test():
    global hs
    hs = TestServer().start()
    print(hs)
    return hs

test = server_test
if __name__ == '__main__':
    test()
