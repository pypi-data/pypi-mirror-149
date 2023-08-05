# This should go in an implementor package, actually.
from xmlrpc.client import ServerProxy, Transport, Fault

def getXmlRpcPythonEvaluator(*args, **kwd):
    return XmlRpcPythonShell(*args, **kwd).evaluateStatement

class AuthTransport(Transport):
    ##    def __init__(self, cookiejar, use_datetime = 0):
    ##        Transport.__init__(self, use_datetime = use_datetime)
    ##        self.cookiejar = cookiejar

    # Use installed cookiejar with urllibl when operating the request.
    ##    def single_request(self, host, handler, request_body, verbose=0):
    ##        pass

    pass

class XmlRpcPythonShell:
    PROTOCOL = 'http'
    PATH = 'RPC2'

    def __init__(self, hostname, port, path = None):
        if path is None:
            path = self.PATH

        transport = None # AuthTransport(cookiejar)
        self.server = ServerProxy('%s://%s:%s/%s' % (self.PROTOCOL,
                                                     hostname, port,
                                                     path),
                                  allow_none = True,
                                  transport = transport)

    def evaluateStatement(self, shell, peer, argstr):
        # todo: a way to exit this evaluator...
        # this should go in the managing command..?
        # xmlrpc-python-connect
        if argstr == 'exit!':
            peer.interpreter.popEvaluator()
            return True

        # todo: asynchronously!!
        try: result = self.server.evaluate(argstr)
        except Fault as fault:
            peer.page_string(fault.faultString)
        else:
            if result:
                if not isinstance(result, str):
                    result = str(result)

                peer.write(result)

        return True

try: from stuphmud.server.player import ACMD
except ImportError:
    ##    from mud.tools import HandleCommandError
    ##    HandleCommandError(full_traceback = True)

    ##    from traceback import print_exc as traceback
    ##    traceback()

    pass

else:
    COMMAND_NAME = 'xmlrpc-python-connect'

    @ACMD(COMMAND_NAME + '*')
    def doXmlRpcPythonConnect(peer, cmd, argstr):
        args = argstr.split() if argstr else ()
        path = None

        if len(args) is 2:
            (hostname, port) = args
        elif len(args) is 3:
            (hostname, port, path) = args
        else:
            print('Usage: %s <hostname> <port> <path>' % COMMAND_NAME, file=peer)
            return True

        pushE = getattr(peer.interpreter, 'pushEvaluator', None)
        if callable(pushE):
            pushE(getXmlRpcPythonEvaluator(hostname, port, path))
            print('Opening XmlRpc Context for [%s:%s]%s%s' % (hostname, port,
                                                                         path and ' on ' or '',
                                                                         path or ''), file=peer)
        else:
            print('Your shell interpreter does not support new evaluators.', file=peer)

        return True
