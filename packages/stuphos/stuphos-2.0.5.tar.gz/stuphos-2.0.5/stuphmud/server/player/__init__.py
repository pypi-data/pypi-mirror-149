# MUD Player Package.
#   -- stuphmud.server.player

# Interpreter aspect.
# todo: rename to 'mud.interface'
from errno import ENOENT
from pickle import load as load_pickle
from pickle import dump as save_pickle
from types import GeneratorType as generator
import platform

from stuphos.etc import ShowFrame, HandleException, logException
from stuphos.etc import getSystemException, isYesValue
from stuphos.etc import capitalize as getCapitalizedName, stylizedHeader
from stuphos.etc.tools.internet import IPAddressGroup

from stuphos import getConfig, invokeTimeoutForHeartbeat, getBridgeModule
from stuphos.runtime import eventResult, DeclareEvent
from stuphos.runtime.registry import getObject

from .events import TriggerPlayerEvent, Trigger

ENTER_GAME_SCRIPT = None # "'player/interpreter/enterGame'(player)"
DEBUG_ENTER_GAME = False # True # Todo: put this in conf under debug-session/core


#@on.newConnection
def interpret(peer):
    from stuphmud.server.player.shell import ShellI
    peer.interpreter = ShellI(commands = getPlayerCommands(peer),
                              scope = getPlayerScope(peer))

    # Install peer.process_telnet_message
    # Install rich editString and messenger

# Greetings.
def getTitleScreen(peer):
    # Full title.
    title = getConfig('title-screen')
    if title:
        try: return open(title).read()
        except IOError as e:
            if e.args[0] != ENOENT:
                HandleException()

def getGreetings(peer):
    # Return the one-liner.
    greetings = getConfig('greetings')
    if greetings:
        greetings = greetings.strip()
        greetings = greetings.replace('%w', ' ')
        greetings = greetings.replace('%n', '\r\n')
        return greetings

def getTitleAndGreetings(peer):
    t = getTitleScreen(peer)
    g = getGreetings(peer)
    return (t + g) if (t and g) else t if t else g if g else ''

def getGreetingDelay(peer):
    try: return float(getConfig('greeting-delay'))
    except (ValueError, TypeError):
        return None

# mud.api.constants
CON_GET_NAME = 'Get name'

def greetPlayer(peer):
    greetings = getTitleAndGreetings(peer)
    if greetings:
        delay = getGreetingDelay(peer)
        if delay:
            def sendGreeting():
                try:
                    if peer.state == CON_GET_NAME:
                        peer.write(greetings)

                except ValueError:
                    # Peer handle no longer valid.
                    pass

            invokeTimeoutForHeartbeat(delay, sendGreeting)

        else:
            peer.write(greetings)

        return eventResult(True)

def welcomePlayer(peer):
    # New player -- Rename to welcomeNewPlayer?
    pass

class playerActivation(DeclareEvent):
    # An event that can be detached from enterGame.
    Module = getBridgeModule()

def postMessages(peer, type, content):
    try: session = peer.session_ref()
    except AttributeError: pass
    else:
        if session is not None:
            session.postMessages([type, content])

def postJavascript(peer, script):
    postMessages(peer, 'javascript', script)
def portalGo(peer, url):
    postMessages(peer, 'portal', url)


def getDefaultStartRoom(actor):
    return 3001
def getLoadRoom(actor):
    return getattr(actor, 'loadroom', None) # saveroom??

def getFirstValidRoom(rooms):
    # XXX this is only valid for the circlemud.world impl.
    # import world; table = world.room.table
    # for vnum in rooms:
    #     try: return table[vnum]
    #     except KeyError:
    #         pass

    from stuphos.system.api import world
    lookup = world.room.lookup

    for vnum in rooms:
        if vnum is not None:
            try: return lookup(vnum)
            except KeyError:
                pass

def getPlayerLoadRooms(actor):
    yield getLoadRoom(actor)
    yield getDefaultStartRoom(actor)

def getStartRoom(avatar):
    return getFirstValidRoom(getPlayerLoadRooms(avatar))


def loggedIn(peer, avatar, webAdapter = False, post = None):
    from stuphos.system.api import mudlog, syslog

    mudlog('%s has logged in (web)' % avatar.name, avatar.level)
    syslog('%s has logged in (web)' % avatar.name)


    # Todo: call player/interpreter/loggedIn, instead of enterGame.
    # That method can initialize location, but the enter-game flow
    # from non-web-adapter main-menu entries needs to be rewritten.
    #
    # Eventually, logged in states differ from enter-game states.

    # Since this isn't done anywhere else during the emerge_internal_peer service call.
    # This should be moved before enterGame.  Do in enterGame.
    avatar.room = getStartRoom(avatar)

    StuphMUD.EnterGame(peer, avatar, webAdapter = webAdapter, post = post)

    # XXX Todo: do this by way of enterGame.
    # self.updateCharacter() # selecting 'Character' in player menu will call do-score command.
    if webAdapter:
        peer.session.updateLocation()


def enterGame(peer, player, webAdapter = False, post = None):
    from stuphos import getConfig
    from stuphos.etc import isYesValue


    # Prioritize activation handlers before triggered event.
    # debugOn()
    playerActivation(peer, player)

    ##    api = getObject('Web::Extension::API')
    ##    if api is not None:
    ##        player.properties = api.getProperties(player)


    if isYesValue(getConfig('converge-spatial')):
        from spatial.spherical.objects import avatar
        # debugOn()
        player.spatial = avatar._layerZero(player)


    TriggerPlayerEvent(player, 'enter-game')


    from stuphmud.server.adapters import MobileAdapter
    player = MobileAdapter(player) # System perspective


    # Enter game script: task.
    from stuphmud.elemental import PlayerScript

    # Todo: configure these based on webAdapter parameter.
    script = configuration.Interpreter.enter_game_script or ENTER_GAME_SCRIPT
    debug = configuration.Interpreter.debug_bridge or DEBUG_ENTER_GAME

    if debug != 'stack':
        debug = isYesValue(debug)

    # debugOn()
    if script:
        if post:
            def initialize(task):
                # From the web adapter login request.
                task.frame.locals['post'] = task.mapping(*post.items())
        else:
            initialize = None

        PlayerScript.evaluateEvent(peer, script,
                                   tracing = debug,
                                   initialize = initialize,
                                   player = player)


    # # Greeting & Enter game script: todo: move into the above evaluateEvent.
    # from stuphos.management import runSessionCore
    # # from stuphos.system.api import syslog

    # name = getConfig('identification', 'Interpreter') or 'identities/{name}'
    # name = name.format(name = peer.avatar.name)
    # # name = 'department/Human Resources/people/' + peer.avatar.name


    # # XXX Race, because we want panel greeting to display first.
    # complete = runSessionCore(peer, name, 'panelGreeting', player = player,
    #                           task_name = '%s:Greeting' % peer.avatar.name)
    # if complete is not None:
    #     @complete
    #     def run(session, result):
    #         session.postMessages(['html-panel', result])

    # complete = runSessionCore(peer, name, 'enterGame', player = player,
    #                           task_name = '%s:EnterGame(Script)' % peer.avatar.name)
    # if complete is not None:
    #     # syslog('complete-core: %r' % complete)

    #     @complete
    #     def run(session, result):
    #         # print(f'javascript: {result}')
    #         # syslog('CUSTOM SCRIPT:\n%s' % result)
    #         # result is from the vm, meaning it got passed through Stack.append
    #         # and probably became a baseStringClass, which the xmlrpc marshaller
    #         # doesn't know how to handle.
    #         session.postMessages(['javascript', str(result)])


    # This runs before the customizers, because they have to wait for the vm.
    # This means the scriptable event, too.  But also this statement is required,
    # and so far there's nothing that makes anything in enterGame rely on the
    # customization code.
    postJavascript(peer, 'enterGame();')


# Rudimentary Access Policy.
TRUSTED_FILENAME = 'etc/trust.python'
class Trust(dict):
    def __init__(self, filename = TRUSTED_FILENAME):
        self.filename = filename
        self.loaded = False

    def load(self):
        try:
            self.update(load_pickle(open(self.filename)))
            self.loaded = True
        except IOError as e:
            from errno import ENOENT
            if e.errno != ENOENT:
                raise

    def save(self):
        save_pickle(self, open(self.filename, 'w'))

    def __contains__(self, avatar):
        not self.loaded and self.load()
        return avatar.idnum == self.get(avatar.name)

    def __iadd__(self, avatar):
        self[avatar.name] = avatar.idnum
        self.save()
        return self

policy = Trust()

# Host Security.
SECURE_DOMAINS = None
TRUST_ALL = False

def getSecureDomains(reload = False):
    global SECURE_DOMAINS, TRUST_ALL
    if SECURE_DOMAINS is None or reload:
        from stuphos import getSection
        securityCfg = getSection('Security')

        # Some builtin domains.
        domains = []
        if isYesValue(securityCfg.get('trust-localhost')):
            # IPv6? Hah!
            try: domains.append(platform.node().lower())
            except: logException(traceback = True)

            domains.append('localhost')
            domains.append('127.0.0.1')

        # Build from config.
        for option in securityCfg.options():
            if option == 'trusted-domain' or \
               option.startswith('trusted-domain.'):
                o = securityCfg.get(option).lower()
                if o == 'all':
                    TRUST_ALL = True
                else:
                    domains.append(o)

        domains = [_f for _f in set(domains) if _f]
        SECURE_DOMAINS = IPAddressGroup(*domains)

    return SECURE_DOMAINS

def isSecureDomain(domainName):
    domains = getSecureDomains()
    if TRUST_ALL:
        return True

    return domainName.lower() in domains

def isFromSecureHost(peer):
    if getattr(peer, 'session', None) is not None:
        # Authenticated via SSL.
        if isYesValue(configuration.Security.trust_web_session_adapter):
            return True

    return isSecureDomain(peer.host)

# Communication Constructs.
class PlayerResponse(Exception):
    pass
class DoNotHere(Exception):
    pass

class PlayerAlert(PlayerResponse):
    def __init__(self, alert):
        self.alert = alert
    def deliver(self, peer):
        # Todo: call customized handler.
        print(self.alert, file=peer)

def playerAlert(fmt, *args):
    raise PlayerAlert(fmt % args)

def HandleCommandError(peer, exc = None, full_traceback = True, error_color = 'r', frame_skip = 1):
    if exc is None:
        exc = getSystemException()

    # First, Cascade to MUD.
    HandleException(exc = exc)

    # Then, send to player.
    name = getattr(exc[0], '__name__', '<Unnamed>')
    tb = exc[2]

    # Skip forward frames as long as possible.
    while frame_skip > 0 and tb.tb_next:
        tb = tb.tb_next
        frame_skip -= 1

    # Configure.
    relative = 'relative' if isYesValue(getConfig('traceback-relative')) else True

    # Find (second to?) last frame.
    while tb.tb_next:
        if full_traceback and tb.tb_next:
            print(ShowFrame(tb.tb_frame, name, use_basename = relative), file=peer)

        tb = tb.tb_next

    print('&%s%s&N' % (error_color, ShowFrame(tb.tb_frame, name, exc, use_basename = relative)), file=peer)

    # Whether or not command error was handled -- which it was.
    return True


# Interactive Organization.
from types import ModuleType
# import new

def getPlayerCommands(peer):
    return getSharedCommands()

def getPlayerScope(peer):
    # Peer connection states are transient at best.
    ##    if hasattr(peer, 'namespace'):
    ##        return peer.namespace

    # Put a persistant namespace module on the avatar,
    # which may exist longer than a network connection.
    try: from world import mobile_instance
    except ImportError: pass
    else:
        a = peer.avatar

        if a and isinstance(a, mobile_instance):
            if hasattr(a, 'namespace'):
                return a.namespace

            ns = a.namespace = ModuleType('mud.player.namespace')
            return ns

    return getSharedScope()

def getSharedCommands():
    from stuphmud.server.player.interfaces import getCommandCenter
    return getCommandCenter(getSharedScope())

def getSharedScope():
    if 'namespace' not in globals():
        global namespace

        namespace = ModuleType('mud.player.namespace')

    return namespace

# Gross -- Scope before Commands?  Decoupled.
# This should just be put in mud.player.interfaces
# (at least i _think_ it's that simple)
shared = getSharedCommands()
ACMD = shared.assignRemoveable # todo: stacked assignment

from stuphos.etc.tools.cmdln import Cmdln, Option
def ACMDLN(verbName, *options, **kwd):
    cmdln = Cmdln(verbName, *options, **kwd)
    if '*' not in verbName:
        verbName += '*'

    def makeCommandHandler(function):
        @ACMD(verbName)
        def doCommand(peer, cmd, argstr):
            try: parsed = cmdln.parseCommand(cmd, argstr)
            except cmdln.HelpExit: return True
            else:
                result = function(peer, parsed)
                if isinstance(result, generator):
                    peer.page('\n'.join(result) + '\n')
                    return True

                return bool(result)

        doCommand.command = function
        return doCommand
    return makeCommandHandler

# todo: ASUBCMD[LN]

def Showing(peer, caption = None, none = None):
    # Use as decorator to generate a paged-string from content and optional caption.
    # Optional 'none' argument shows this as string if no results were obtained.
    def showResults(results):
        def s():
            if caption:
                yield stylizedHeader(caption)

            for r in results:
                yield r

            yield ''

        peer.page('\r\n'.join(s()))

    if none:
        def showOrNone(view):
            results = list(view())
            if results:
                showResults(results)
            else:
                print(none, file=peer)

            return view

        return showOrNone

    def show(view):
        showResults(view())
        return view

    return show
