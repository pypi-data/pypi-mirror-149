# XDebug front-end.
from socketserver import ThreadingTCPServer, StreamRequestHandler
from xml.dom.minidom import parseString
from io import StringIO as NewBuffer
from _thread import start_new_thread as nth

from stuphos.runtime.facilities import Facility
from stuphos import enqueueHeartbeatTask, executeInline
from .wizard import parameters

from stuphos.system.api import mudlog
import imp


DBGP_COMMANDS = \
'''&yDGBp Commands&N
&r=============&N
breakpoint_list
breakpoint_{get,remove,update} -d <name>
  update: -s {enabled,disabled}
          -o {>=,==,%}
          -n <line-number>
          -h <hit-value>

breakpoint_set
  -t {line,conditional,call,return,exception,watch}
  -n <line-number>
  -f <file-name>
  -m <function-name>
  -a <class-name>
  -x <exception-name>
  -s {enabled,disabled}
  -o {>=,==,%}
  -h <hit-value>
  -r <integer>
  -- <conditional-expression>

context_names
context_get
  -c <context # (integer)>
  -d <depth (integer)>

eval
  -p <page (integer)>
  -- <expression>

feature_{get,set}
  -v <value>
  -n {breakpoint_{languages,types},data_encoding,encoding,
      language_{name,supports_threads,version},
      max_{children,data,depth}, protocol_version,
      supported_encodings, supports_{async,postmortem},
      show_hidden}

typemap_get
property_{get,set,value}
  -d <depth (integer)>
  -c <context # (integer)>
  -p <page (integer)>
  -m <max data (integer)>
  -n <name>

  set: -t {bool,int,float,string}

source
  -f <file-name>
  -b <begin (integer)>
  -e <end (integer)>

stack_depth
stack_get
  -d <depth (integer)>

status
stderr
stdout
  -c {0,1}

run
step_{into,out,over}
stop
detach
xcmd_{profiler_name_get,get_executable_lines}
'''

class XDebugServer(Facility, ThreadingTCPServer):
    NAME = 'XDebug::Server'

    BIND_HOST = 'localhost'
    BIND_PORT = 9000

    class Manager(Facility.Manager):
        MINIMUM_LEVEL = Facility.Manager.IMPLEMENTOR
        VERB_NAME = 'xdebug*'

        def do_bind(self, peer, cmd, args):
            s = self.facility.get()
            if s is not None:
                if len(args) == 1:
                    key = args[0]
                    session = s.getSession(key)
                    if session is None:
                        print('Unknown session: %r' % key, file=peer)
                    else:
                        if session.isListening(peer):
                            print('Already listening to %s.' % key, file=peer)
                        else:
                            session.bind(session.PeerListener(peer))
                            print('Binded to %s.' % key, file=peer)

        def do_reload(self, peer, cmd, args):
            self.facility.destroy()
            module = imp.reload(__import__(__name__, globals(), locals(), ['']))
            self.facility.get(create = True)

            print(module, file=peer)

        def do_commands(self, peer, cmd, args):
            peer.page_string(DBGP_COMMANDS)

    @classmethod
    def create(self):
        return self((self.BIND_HOST, self.BIND_PORT),
                    self.XDebugDBGpRequestHandler)

    def __init__(self, binding, rqh):
        self.sessions = {}
        ThreadingTCPServer.__init__(self, binding, rqh)
        nth(self.serve, ())

    def serve(self):
        self.__running = True
        while self.__running:
            self.handle_request()

    def server_stop(self):
        self.__running = False
        self.server_close()

    def __registry_delete__(self):
        self.server_stop()

    def getStatus(self):
        sessions = '\n  '.join('%s -- %s' % (key, s) for (key, s) in self.sessions.items())
        return '%s (%s)%s%s\n' % (self.NAME, self.__class__.__name__,
                                sessions and ':\n  ' or '', sessions)

    def log(self, message):
        mudlog('[%s] %s' % (self.NAME, message))

    # Session Management.
    def addSession(self, key, requestHandler):
        if key not in self.sessions:
            self.sessions[key] = self.Session(key, requestHandler)
            self.log('New Session: %r' % key)

    def removeSession(self, key):
        if key in self.sessions:
            del self.sessions[key]
            self.log('Session Complete: %r' % key)

    def getSession(self, key):
        return self.sessions.get(key)

    class Session:
        class PeerListener:
            def __init__(self, peer):
                self.peer = peer
            def __eq__(self, other):
                return self.peer == other

            def notify(self, msg):
                try: m = self.peer.xdebug_messages
                except AttributeError:
                    m = self.peer.xdebug_messages = []

                m.append(msg)
                self.peer.page_string(describeMessage(msg))

        def __init__(self, key, requestHandler):
            self.key = key
            self.requestHandler = requestHandler
            self.listeners = []

        def isListening(self, object):
            for o in self.listeners:
                if o == object:
                    return True

        def bind(self, object):
            self.listeners.append(object)

        def sendCommand(self, command, args):
            self.requestHandler.sendCommand(self.key, command, args)

        def handleResponse(self, message):
            def sendNotifications():
                for o in self.listeners:
                    o.notify(message)

            enqueueHeartbeatTask(sendNotifications)

        def __str__(self):
            return ', '.join('%s=%r' % (name, value) for (name, value) in \
                             ((name, getattr(self, name, None)) for name in \
                              XDebugServer.INIT_VALUES) if value is not None)

    INIT_VALUES = ('protocol_version', 'language', 'appid', 'fileuri')

    # DBGp protocol
    class XDebugDBGpRequestHandler(StreamRequestHandler):
        def handle(self):
            # Read first message to initialize the session.
            init = self.readMessage().getElementsByTagName('init')[0]
            idekey = str(init.getAttribute('idekey'))

            executeInline(self.server.addSession, idekey, self)
            session = self.server.getSession(idekey)
            for name in XDebugServer.INIT_VALUES:
                setattr(session, name, str(init.getAttribute(name)))

            # Read all following message responses and forward to facility management.
            for msg in self:
                session.handleResponse(msg)

            executeInline(self.server.removeSession, idekey)

        def sendCommand(self, key, command, args):
            payload = [command, '-i', key]
            if args: payload.append(args)
            payload = ' '.join(payload)
            payload += '\x00'
            self.wfile.write(payload)

        def __iter__(self):
            while True:
                msg = self.readMessage()
                if msg is None:
                    break

                yield msg

        def readMessage(self):
            msg = self.readXmlMessage(self.rfile)
            if msg is not None:
                return parseString(msg)

        # what about socket.error: errno 104 Connection reset by peer?
        def readXmlMessage(self, conn):
            size = self.readMessageSize(conn)
            if size is not None:
                msg = conn.read(size)
                conn.read(1) # null-byte
                return msg

        def readMessageSize(self, conn):
            buf = ''
            while True:
                c = conn.read(1)
                if c == '':
                    break

                if c == '\x00':
                    return int(buf)

                buf += c

def describeMessage(msg):
    docEl = msg.documentElement
    if docEl.tagName == 'response':
        attrs = '\r\n'.join('%s: %s' % (str(attr.name).capitalize(), str(attr.value)) \
                            for attr in list(docEl.attributes.values()) \
                                if attr.name != 'xmlns' and attr.prefix is None)

        nodes = '\r\n'.join(getNodeValue(node) for node in docEl.childNodes)

        return '%s\r\n%s\r\n' % (attrs, nodes)

    elif docEl.tagName == 'stream':
        encoding = docEl.getAttribute('encoding')
        return ('Encoding: %s\r\n' +
                'Type: %s\r\n' +
                '%s\r\n') % (encoding, docEl.getAttribute('type'),
                             getTextContent(docEl).decode(encoding))

    return msg.toprettyxml()

def getNodeValue(node):
    if node.tagName == 'property':
        type = node.getAttribute('type')
        size = node.getAttribute('size')
        address = node.getAttribute('address')

        # string
        encoding = node.getAttribute('encoding')

        # array
        numChildren = node.getAttribute('numchildren')
        page = node.getAttribute('page')
        pagesize = node.getAttribute('pagesize')

        # array, object
        children = node.getAttribute('children')

        # and: 'name'
        # type: bool, int, float, string, null, array, object, property
        # type: resource, null

        value = getTextContent(node)
        if encoding == 'base64':
            value = value.decode('base64')

        # todo: array types have child nodes...

        return '%s\r\n%s' % ('\r\n'.join('%s: %s' % (str(name).capitalize(), str(value)) for (name, value) in \
                             [_f for _f in [('type', type), ('size', size), ('address', address),
                               ('encoding', encoding), ('page', page), ('pageSize', pagesize),
                               ('children', children), ('numChildren', numChildren)] if _f]),
                             value)
                
    return node.toprettyxml(indent = '  ') 

def getTextContent(node):
    return ''.join(c.data for c in node.childNodes \
                   if c.nodeType in (c.TEXT_NODE, c.CDATA_SECTION_NODE))

# Install.
XDebugServer.manage()
# XDebugServer.get(create = True)

# Wizard Control.
def getServerSession(key):
    server = XDebugServer.get()
    if server is not None:
        return server.getSession(key)

@parameters(2, None)
def doXDebug(peer, key, command, *args):
    session = getServerSession(key)
    if session is not None:
        # Some command preprocessing:
        if command == 'eval':
            i = args.index('--')
            assert i >= 0
            code = ' '.join(args[i+1:])
            code = code.encode('base64')

            args = list(args[:i+1])
            args.append(code)

        # Dispatch the command to the session.
        session.sendCommand(command.replace('-', '_'), ' '.join(args))
