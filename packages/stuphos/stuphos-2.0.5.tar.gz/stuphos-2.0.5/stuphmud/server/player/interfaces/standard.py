# Standard implementation of Command Manager.
__all__ = ['StandardCommandManager']

from stuphmud import server as mud

from stuphmud.server.player.interfaces import CommandCenter
from stuphos.etc.tools import getLineFromCache, functionLines, functionName
import imp

SYSLOG_FILE = '../log/syslog'
def readSyslog():
    from os import getenv
    file = getenv('STUPH_LOGFILE', SYSLOG_FILE)
    return filterSyslog(open(file).read())

def filterSyslog(text):
    return text.replace('\x00', '').replace('\n', '\r\n')

##  try: from mud.tools import functionLines, functionName
##  except ImportError:
##      def notimpl(*args, **kwd):
##          raise NotImplementedError
##
##      functionLines = functionName = notimpl

def listCommands(commands):
    # Generates two-column lines.
    commandMap = dict()
    for v in list(commands.values()):
        commandMap[v] = list()

    # Collect names for each function -- Inversion.
    for (k, v) in commands.items():
        commandMap[v].append(k)

    # Go through each function, generating a listing for all the names and descr of func.
    for (func, names) in commandMap.items():
        func = func.current # registration
        try: func = func.command
        except AttributeError:
            pass

        doc = func.__doc__ or ''
        if doc:
            doc = doc.replace('\n', '')

        # yield functionName(func), doc
        yield func.__name__, doc

        # Zip side-by-sides.
        names.sort() # Alphabetically
        desc = list(map(str, functionLines(func, max = len(names), trim_decorators = True)))

        for (a, b) in sideBySide(names, desc):
            yield '    ' + a, b

    # Generate empty line.
    yield ('', '')

def sideBySide(a, b):
    '(unzip list-first-column list-second-column)'

    la = len(a)
    lb = len(b)

    for x in range(la):
        # Python 2.6 syntax capability:
        # i = a[x] if x < la else ''
        # j = b[x] if x < lb else ''
        if x < la:
            i = a[x]
        else:
            i = ''

        if x < lb:
            j = b[x]
        else:
            j = ''

        yield i, j

class StandardCommands(CommandCenter):
    'Some sample standard commands provided here.'
    # Only compatible with a CmdDict multiple-inheritance.

    # @MinimumLevel(LVL_IMPL)
    # @Qualifier(lambda peer, *args:peer.avatar and peer.avatar.implementor)
    @staticmethod
    def doPageSyslog(peer, cmd, argstr):
        'Page the ENTIRE SYSLOG!!'

        if peer.avatar and peer.avatar.implementor:
            peer.page(readSyslog())
            return True

    @staticmethod
    def doShowBridgedEvents(peer, cmd, argstr):
        'Display aspects on bridged mud events.'

        if peer.avatar and peer.avatar.implementor:
            from stuphos.system.api import game
            from stuphmud.server import bridge

            bridge.showBridgedEvents(game.bridgeModule(), page = peer.page, endline = '\r\n')
            return True

    @staticmethod
    def doShowHeartbeatTasks(peer, cmd, argstr):
        'Show heartbeat tasks.'

        if peer.avatar and peer.avatar.implementor:
            from stuphmud.server import tasks
            tasks.show(peer.page)
            return True

    @staticmethod
    def doReloadInterpreter(peer, cmd, argstr):
        'Reload the player module, all the interpretation, and re-interpret player.'

        if peer.avatar and peer.avatar.implementor:
            from stuphmud.server import player
            imp.reload(player).interpret(peer)
            return True

    def doShowCommands(self, peer, cmd, argstr):
        'Displays command listing of this object.'

        # Generate lines to be printed side-by-side with names.
        width = 30, 80
        fmt   = '%%-%(left)d.%(left)ds %%-%(right)d.%(right)ds' % {'left':width[0], 'right':width[1]}

        peer.page('\r\n'.join(fmt % line for line in listCommands(self.c)) + '\r\n')
        return True

    def doCassiusConnection(self, peer, cmd, argstr):
        if peer.avatar and peer.avatar.supreme:
            cas = self.openCassius()

            # Python 2.6 syntax capability:
            # argstr = argstr.strip() if argstr else ''
            argstr = argstr and argstr.strip() or ''

            if argstr == 'close':
                # Delete installation known to mud, and our cas builtin.
                del builtin.cassius_connection, builtin.cas

                print('&D >&N', cas, 'Deleted!', file=peer)
                return True

            if argstr == 'reopen':
                del builtin.cassius_connection, builtin.cas

                # Re-open and fall thru...
                # reload(telnet)
                cas = self.openCassius()

            elif argstr == 'bind':
                cas.adapters.add(telnet.bind(peer))

                print('Okay.', file=peer)
                return True

            elif argstr == 'unbind':
                print('No idea how to do that!', file=peer)
                return True

            elif argstr:
                # Send to connection.
                cas.sendline(argstr)

                print('&D >&N', argstr, file=peer)
                return True

            print(cas, file=peer)
            return True

        # Not supreme, not allowed!

    def doMainMenu(self, peer, cmd, argstr):
        mainMenu = mud.player.namespace.getGlobals().get('Menu')
        if not mainMenu:
            from person.menu import Main as mainMenu

        return True

    # These have just gone obselete.
    # def setup(self):
    #     # CommandSetup.setup(self)
    #     a = self.insertOverridingAll

    #     a('page-*syslog',          self.doPageSyslog        )
    #     a('show-br*idged-events',  self.doShowBridgedEvents )
    #     a('show-t*asks',           self.doShowHeartbeatTasks)
    #     a('reload-*interpreter',   self.doReloadInterpreter )
    #     a('interpret*',            self.doReloadInterpreter )
    #     a('show-comm*ands',        self.doShowCommands      )
    #     a('main*-menu',            self.doMainMenu          )

# Export this:
##  class StandardCommandManager(CommandManager):
##      'Implements a command manager (abbreviation-managed command dictionary) with standard commands.'
##
##      def setup(self):
##          StandardCommandMixin.setup(self)
##
##          try:
##              # self.importCommands('commands')
##              self.importCommands('mud.player.interfaces.commands')
##
##          except ImportError:
##              pass
##
##      def __init__(self, *args, **kwd):
##          CommandManager.__init__(self, *args, **kwd)
