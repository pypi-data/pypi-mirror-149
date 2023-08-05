# Copyright 2011 Clint Banis.  All rights reserved.
# Telnet Message Dispatch.
#
r"\xff\x0fI44.JSON:['CREATE','FILE-SCRIPT.PY','\"Document\"']\xff\x0f"

from stuphmud.server.player import playerAlert, PlayerAlert, getCapitalizedName
from stuphmud.server.player import HandleCommandError as HandleTelnetError

from stuphos.etc.tools import reraiseSystemException
from functools import reduce

class TelnetMessenger:
    def process(self, peer, msg):
        # Peer Head -- Telnet Message
        #
        # Also of note: the result of this method generally propogates back up to
        # the Network::getCommand (EventBridge), and returning < 0 will prevent any
        # further commands from being processed during that cycle.
        try:
            # todo: build in message digest auth here! (while we still have payload)
            msg = self.loadMessage(msg)
            if type(msg) in (list, tuple) and len(msg) > 0:
                # Here: Beware returning this value..? Affects network flow.
                self.dispatch(peer, msg[0], msg[1:])
            else:
                # Or syslog..?  no, back to where it started from.
                playerAlert('Unknown message type/length: %s', type(msg).__name__)

        except PlayerAlert as e:
            e.deliver(peer)
        except:
            # To syslog... This is more of a system error.
            from stuphmud.server.player import HandleCommandError as HandleTelnetError
            HandleTelnetError(peer)

    def loadMessage(self, msg):
        # First dereference the string buffer.
        msg = msg.getvalue()

        if msg.startswith('JSON:'):
            from simplejson import loads
            msg = loads(msg[5:])
        elif msg.startswith('PICKLE:'):
            from pickle import loads
            msg = loads(msg[7:])
        elif msg.startswith('XMLRPC:'):
            from xmlrpc.client import loads
            (params, method) = loads(msg[7:])

            # Flatten parameters into one list.
            msg = [method]
            msg.extend(params)

        elif msg.startswith('PTCL:'): # PNTL? RCTL?
            return ['pentacle:command', msg[5:]]

        elif msg.startswith('HTTP:'):
            playerAlert('Unable to process HTTP request.')

        return msg

    def getDispatchAction(self, operation):
        if self.dispatch_module is not None:
            # First treat the module as a delegate.
            delegate = getattr(self.dispatch_module, 'getDispatchAction', None)
            if callable(delegate):
                return delegate(operation)

            # Otherwise, perform string lookups.
            if type(operation) is not str:
                playerAlert('Unknown operation type: %s', type(operation).__name__)

            actionName = '_do%s' % getCapitalizedName(operation)
            action = getattr(self.dispatch_module, actionName, None)
            if callable(action):
                return action

            ##    action = getattr(self.dispatch_module, operation, None)
            ##    if callable(action):
            ##        return action

    def dispatch(self, peer, operation, params):
        action = self.getDispatchAction(operation)
        if callable(action):
            return action(peer, *params)
        else:
            playerAlert('Unknown operation: %r' % operation)

    @classmethod
    def isInstalled(self, peer):
        pcs = getattr(peer, 'process_telnet_message', None)
        if pcs is not None:
            x = getattr(pcs, '__class__', None)
            if x and issubclass(x, self):
                return True
            x = getattr(pcs, 'im_class', None)
            if x and issubclass(x, self):
                return True

    def __init__(self, peer, dispatch_module):
        self.dispatch_module = dispatch_module
        self.install(peer)

    def install(self, peer):
        peer.process_telnet_message = self
    def uninstall(self, peer):
        try: del peer.process_telnet_message
        except AttributeError: pass

    def __call__(self, *args, **kwd):
        return self.process(*args, **kwd)
    def __repr__(self):
        return '%s (%r)' % (self.__class__.__name__, self.dispatch_module)

    __str__ = __repr__

def isProcessorInstalled(peer):
    return TelnetMessenger.isInstalled(peer)
def installProcessor(peer, *args, **kwd):
    TelnetMessenger(peer, *args, **kwd)
def uninstallProcessor(peer):
    try: pcs = peer.process_telnet_message
    except AttributeError: pass
    else:
        try: pcs.uninstall(peer)
        except AttributeError:
            del peer.process_telnet_message

# Interface.
from stuphmud.server.player import ACMD

@ACMD('teln*et-control')
def doManageTelnetControl(peer, cmd, argstr):
    args = (argstr or '').split()
    larg = len(args) and args[0].lower() or ''

    if larg in ('', 'status', 'show'):
        target = peer
        if len(args) == 2 and peer.avatar and peer.avatar.level >= 115:
            name = args[1]
            target = peer.avatar.findplayer(name, False, False)
            if not target:
                print('Player %r not found.' % name, file=peer)
            elif not target.peer:
                print('%s is not logged in.' % target.name, file=peer)
                target = None
            else:
                print('Telnet status for: %s' % target.name, file=peer)
                target = target.peer

        if target is not None:
            print('Processor is %sinstalled.' % \
                  (not isProcessorInstalled(target) and 'not ' or ''), file=peer)

            conv = getattr(target, 'telnet_conversation', None)
            if conv is not None:
                size = conv.message_size
                done = size - conv.message_left
                percent = (done / float(size)) * 100

                print('Message progress: %d/%d (%d%%)' % (done, size, percent), file=peer)
                buf = conv.message_buf
                if buf is not None:
                    print('Message sample: %r' % buf.getvalue()[:60], file=peer)

    elif larg == 'manage':
        if not isProcessorInstalled(peer):
            installProcessor(peer, getDefaultDispatchModule())
            print('Processor installed.', file=peer)
        else:
            print('Already managed.', file=peer)

    elif larg == 'cancel':
        if isProcessorInstalled(peer) >= 2 or len(args) == 2 and args[1] == 'force':
            uninstallProcessor(peer)
            print('Processor uninstalled.', file=peer)
        else:
            print('Not currently managing.', file=peer)

    elif larg == 'flush':
        delattr(peer, 'telnet_conversation')
        print('Flushed.', file=peer)

    else:
        print('Unknown subcommand: %r' % larg, file=peer)

    return True

# Dispatch Groups.
class Organized:
    def __init__(self, *modules, **kwd):
        modules = list(modules)
        self.modules = {'': modules}

        # Overload by prefixed name, retaining default.
        m = kwd.get('')
        if hasattr(m, 'extend'):
            m.extend(modules)

        self.modules.update(kwd)

    def getDispatchAction(self, name):
        # Todo: complexify the prefixed qualifier.
        i = name.find(':')
        if i >= 0:
            section = name[:i]
            name = name[i+1:]
        else:
            section = ''

        for m in self.modules.get(section, []):
            action = m.getDispatchAction(name)
            if action is not None:
                return action

    def addModule(self, module, prefix = None):
        prefix = prefix or ''
        m = self.modules.get(prefix)
        if m is None:
            m = self.modules[prefix] = []

        m.append(module)

    def __getitem__(self, name):
        return list(self.modules.get(name, []))
    def __repr__(self):
        return '%s (%s)' % (self.__class__.__name__,
                            ', '.join(list(self.modules.keys())))

    __str__ = __repr__


# Todo: write a decoupled registration api.
DEFAULT_MODULES = \
    dict(ftp = 'mud.player.telnet.ftp.FTPDispatchModule',
         rexec  = 'mud.player.telnet.rexec.RExecDispatchModule',
         # deploy = 'mud.player.telnet.deploy.LiveDeployDispatchModule',
         # http = 'mud.player.telnet.http',
         # pentacle = 'mud.player.telnet.pentacle',
         )

def _getDefaults():
    from stuphos import getSection
    section = getSection('TelnetModules')
    options = tuple((n, section.get(n)) for n in section.options())
    return options or iter(DEFAULT_MODULES.items()) # todo: merge opts with builtins?

def findDispatchModule(name):
    # A straight import will fail if the trailing members are not modules.
    # return __import__(name, globals(), locals(), fromlist = [''])

    try: module = __import__(name)
    except ImportError as e:
        e = str(e)
        if e.startswith('No module named '):
            fail = e[16:]
            if name.endswith(fail):
                major = name[:-(len(fail) + 1)]
                module = __import__(major)
            else:
                reraiseSystemException()
        else:
            reraiseSystemException()

    def getModuleMember(module, name):
        return getattr(module, name)

    parts = name.split('.')
    return reduce(getModuleMember, parts[1:], module)

def buildDefaultDispatchModule():
    dispatch = Organized()
    for (prefix, name) in _getDefaults():
        prefix = prefix.strip()
        if prefix.lower() == 'default':
            prefix = ''

        module = findDispatchModule(name)
        if module is not None:
            # Note: this is not a factory; use the class found.
            dispatch.addModule(module, prefix = prefix)

    return dispatch

from types import ClassType, MethodType, TypeType
class DispatchModuleBase:
    # Base implementation for pluggable subclasses.
    @classmethod
    def getDispatchAction(self, action):
        method = getattr(self, '_do%s' % getCapitalizedName(action), None)
        if type(method) is (ClassType, TypeType):
            # Hmm, kind of weird, but it's for modules that implement their
            # action handlers like so:
            #    class _doAction(object):
            #        def __new__(self, peer, *params):
            #            return 'result'
            #
            return method

        if callable(method):
            return MethodType(method, self())

    def _validateMessage(self, digest, key, *parts):
        return ValidateMessage(digest, key, *parts)

    def _loadKeyfile(self, keyfile):
        return LoadKeyfile(keyfile)

import hmac
def ValidateMessage(digest, key, *parts):
    hash = hmac.new(key)
    for p in parts:
        hash.update(p)

    return hash.hexdigest() == digest

def LoadKeyfile(keyfile):
    # As passphrase.
    return open(keyfile).read().strip()

# Shared COM -- todo runtime registry access.
TELNET_DISPATCH_MODULE = 'Telnet::DispatchModule::Default'
def getDefaultDispatchModule():
    from stuphos.runtime.registry import getObject
    return getObject(TELNET_DISPATCH_MODULE,
                     create = buildDefaultDispatchModule)

@runtime.api('Telnet::Dispatch::API')
class TelnetDispatchAPI:
    @classmethod
    def RegisterModuleClass(self, prefix):
        def registerAs(moduleClass):
            DEFAULT_MODULES[prefix] = '%s.%s' % \
                (moduleClass.__module__, moduleClass.__name__)

            return moduleClass
        return registerAs
