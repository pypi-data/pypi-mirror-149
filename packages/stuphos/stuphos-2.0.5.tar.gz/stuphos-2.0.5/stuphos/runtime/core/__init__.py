# Now a ph component that provides a runtime configuration.
#
# Separate from the framework/compartment core, used in an embedding context.
# Also separate from the (legacy) mud package that resides now in application.server.
#
# Copyright 2022 runphase.com .  All rights reserved.
# --

# MUD Runtime Core.
#    mud.runtime.core provides:
#       * access to the event bridge
#       * programming the virtual machine
#       * configuration access
#       * boot procedure
#
# This should probably be called 'bootstrap' (the runtime is the core)
from stuphos.runtime import BINDINGS, EVENT_NAMES, loadOnto, Binding
from stuphos.etc.tools.logs import *

from stuphos.management.config import PackageManager, getParentPath, joinpath
from stuphos.management.config import getStandardPath, loadConfig

from stuphos.runtime.registry import getObject as getRegistryObject
from stuphos.runtime.registry import delObject as deleteRegistryObject
from stuphos.runtime.registry import RegistryNotInstalled

from stuphos.runtime.plugins import installPlugins

from stuphos.etc.tools import isYesValue, isNoValue

__version__ = 0.9

DEFAULT_TASKPOOL_MAXSIZE = 4


def getBridgeModule():
    ##    # First code to load the game module.
    ##    from pdb import run
    ##    run('from game import bridgeModule')

    from stuphos.system.api import game
    return game.bridgeModule()

def callEventBridge(name, *args, **kwd):
    try: event = getattr(getBridgeModule(), name)
    except AttributeError: pass
    else:
        if callable(event):
            return event(*args, **kwd)

def getMudModule():
    from stuphmud import server as mud
    return mud

def getHeartbeat():
    return getBridgeModule().heartbeat

def enqueueHeartbeatTask(*args, **kwd):
    return getHeartbeat().enqueueHeartbeatTask(*args, **kwd)
def deferredTask(*args, **kwd):
    # print(f'deferring task to heartbeat... {args}')
    return getHeartbeat().deferredTask(*args, **kwd)

enqueue = enqueueHeartbeatTask
executeInline = deferredTask

def inline(function):
    # Decorator
    def inlineWrapper(*args, **kwd):
        # print(f'inlining... {args}')
        return executeInline(function, *args, **kwd)

    try: inlineWrapper.__name__ = function.__name__
    except AttributeError: pass

    try: inlineWrapper.__doc__ = function.__doc__
    except AttributeError: pass

    return inlineWrapper

def invokeTimeoutForHeartbeat(timeout, function, *args, **kwd):
    return getHeartbeat().invokeTimeoutForHeartbeat(timeout, function, *args, **kwd)
def invokeTimeout(timeout, function, *args, **kwd):
    return getHeartbeat().invokeTimeout(timeout, function, *args, **kwd)

CONFIG_OBJECT_NAME = 'MUD::Configuration'
CONFIG_FILE = getStandardPath('etc', 'config.cfg')

def _createMUDConfig():
    from ...etc.tools import registerBuiltin
    o = loadConfig(CONFIG_FILE)
    registerBuiltin(o.addressor, 'configuration')
    registerBuiltin(runtime.MUD.Configuration, 'mudConfig')
    return o

def getConfigObject():
    # return mudConfig(loadConfig, CONFIG_FILE)
    return getRegistryObject(CONFIG_OBJECT_NAME,
                             create = _createMUDConfig)

def deleteConfig():
    # del runtime[mudConfig]
    return deleteRegistryObject(CONFIG_OBJECT_NAME)

def reloadConfigFile(filename):
    global CONFIG_FILE
    CONFIG_FILE = filename
    deleteConfig()

def getConfig(name, section = 'MUD'):
    try: return getConfigObject().get(name, section = section)
    except RegistryNotInstalled: pass
def getSection(section = 'MUD'):
    try: return getConfigObject().getSection(section)
    except RegistryNotInstalled: pass


# Boot Procedure.
SITE_PATH = getParentPath(__file__, 5) # XXX ???
COMPONENTS_FILE = 'components.pth'

# EASY_SITE_PATH = joinpath(SITE_PATH, 'packages/third-party')
# EASY_INSTALL_FILE = 'easy-install.pth'

def getDefaultComponentsPath():
    return SITE_PATH, COMPONENTS_FILE

def installSite():
    # Manually search non-standard paths for .pth files.
    path = getConfig('components')
    if path is None:
        (path, file) = getDefaultComponentsPath()
    else:
        from os import sep
        i = path.rfind(sep)
        if i < 0:
            file = path
            path = '' # '.'
        else:
            file = path[i+1:]
            path = path[:i]

    PackageManager(path, file).install()
    # PackageManager(EASY_SITE_PATH, EASY_INSTALL_FILE).install()

def installBridge():
    bridgeModule = getBridgeModule()
    thisModule = getMudModule()

    # from mud.runtime import declare, DeclareEvent
    # declare(bridgeModule, EVENTS)
    loadOnto(BINDINGS, bridgeModule)

    thisModule.on = Binding(bridgeModule)
    thisModule.core = Binding(thisModule)

    ##    class bootStart(DeclareEvent):
    ##        Module = thisModule
    ##    class bootComplete(DeclareEvent):
    ##        Module = thisModule

    return bridgeModule

def installHost():
    from socket import error
    from errno import EADDRINUSE

    disabling = [EADDRINUSE]

    # error: [Errno 10013] An attempt was made to access a socket in a way forbidden by its access permissions
    try: from errno import WSAEACCES
    except ImportError: pass
    else: disabling.append(WSAEACCES)

    try:
        from stuphos.kernel import getHost
        from stuphos.kernel import NotConfigured
        try: getHost(create = True).start()
        except NotConfigured:
            logWarning('XMLRPC disabled.')

    except error as e:
        if e.args[0] not in disabling:
            from stuphos.etc.tools import reraiseSystemException
            reraiseSystemException()

        logWarning('Host port is in use -- XMLRPC disabled.  Please reconfigure!')

    except Exception:
        logException(traceback = True)


def installEnviron():
    # Configure the system/shell environment.
    from os import environ
    envCfg = getSection('Environment')
    for name in envCfg.options():
        environ[name] = envCfg.get(name)

def installSystemComponents():
    # Install system path components.
    systemComp = getSection('SystemComponents')
    systemPaths = []

    if systemComp is not None:
        for option in systemComp.options():
            if option == 'system-path' or \
               option.startswith('system-path.'):
                systemPaths.append(systemComp.get(option))

    from sys import path as syspathCore
    for path in systemPaths:
        if path not in syspathCore:
            syspathCore.append(path)

def installSystemPackages():
    systemPkgs = getSection('SystemPackages')
    packages = []

    if systemPkgs is not None:
        for option in systemPkgs.options():
            if option == 'package' or \
               option.startswith('package.'):
                pkg = systemPkgs.get(option)
                # todo: filter for duplicate packages?
                packages.append((option, pkg))

    for (n, pkg) in sorted(packages, key = lambda a_b: a_b[0]):
        try: __import__(pkg)
        except SyntaxError as e:
            print(f'[syntax error] {pkg}: {e}')

        except: logException(traceback = True)


class log(object):
    '''
    log.memory.new_environment(id(memory), self.__class__.__name__)

    '''

    @classmethod
    def _nullreceiver(*parameters):
        pass

    def __init__(self, receiver):
        self._receiver = receiver
    def __call__(self, *parameters):
        return self._receiver(*parameters)

    def __getattr__(self, parameter):
        try: return object.__getattribute__(self, parameter)
        except AttributeError:
            return self._parameter(self, parameter)

    class _parameter(list):
        def __init__(self, log, *parameters):
            self._log = log
            list.__init__(self, *parameters)

        def __call__(self, *parameters):
            return self._log(*self)

        def __getattr__(self, name):
            try: return object.__getattribute__(self, name)
            except AttributeError:
                return self.__class__(self._log, *(self + (name,)))


def installJournal():
    try:
        from stuphos.management import syslog
        syslog.Journal.get(create = True)
    except:
        logException(traceback = True)


def installServices(thisModule):
    # Install VM
    # Install system paths
    # Install environ config
    # Install XMLRPC host service
    # Install journal
    # Import system modules (config)
    # Install Management modules
    # Install logging service

    # Create binding to bridge module.

    # Todo: actually make this a registered COM object!
    if not isYesValue(configuration.VM.disabled):
        try: from stuphos.kernel import Machine, Native
        except ImportError:
            logException(traceback = True)
        else:
            bridge = getBridgeModule()
            bridge.heartbeat = Machine()

            runtime.System.Network.Core(lambda:thisModule)
            runtime.System.Bridge(lambda:bridge)
            runtime.System.Engine(lambda:bridge.heartbeat)

            debug = configuration.AgentSystem.debug_natives

            if isYesValue(debug):
                Native._tracing = True
            elif debug is not None and isNoValue(debug):
                Native._tracing = False

            try: from stuphos.kernel import pool
            except ImportError: pass
            else:
                cfg = configuration.TaskPool
                pool = pool(initial_size = int(cfg.initial_size or 0),
                            max_size = int(cfg.max_size or DEFAULT_TASKPOOL_MAXSIZE))

                runtime.System.Engine.Pool(lambda:pool)


    # runtime.components = registry.Access(runtime, 'registry')
    # runtime.builtin = builtin
    # builtin.runtime = runtime
    # runtime.system = builtin.system
    #     # runtime.system.core

    # runtime.core = runtime.system.module.stuphos ?
    #     runtime.core.mud = runtime.system.module.stuphos ?
    #     runtime.core.game = runtime.system.module.game
    #     runtime.core.world = runtime.system.module.world


    # Pre-Management Set:
    installSystemComponents()
    installEnviron()
    installHost()

    installJournal()

    # Note that this relies on core components working.
    # But the rest of the runtime should rely on system
    # packages, not the other way around.
    installSystemPackages()

    try: from stuphos.management import initForCore
    except ImportError: pass
    else:
        # Hack -- fixup core plugins before managed components.
        try:
            import stuphmud.server.player.db.managedfs
            from stuphmud.server.player.commands.gc import wizard
        except:
            # XXX Why doesn't this print the exception causes?
            # import traceback
            # traceback.print_exc()

            logException(traceback = True)

        initForCore()

    try: from stuphmud.server.player.interfaces.code.girl import initCommands
    except ImportError: pass
    else: initCommands()

    # Todo: integrate this into management initForCore?
    # installSystemPackages() # XXX this should probably be before initForCore, simply because core world init might rely on a more initially-loaded module.
    # debugOn()
    installPlugins()


    try:
        from stuphos.kernel import MachineCore
        MachineCore.systemCore()
    except:
        logException(traceback = True)


    endpoint = getConfig('log-endpoint', 'MUD')
    receiver = log._nullreceiver
    if endpoint:
        from xmlrpclib import ServerProxy
        receiver = ServerProxy(endpoint).logging.receive

    from ...etc.tools import registerBuiltin
    registerBuiltin(log(receiver), 'log')


def installWorld():
    try: from stuphmud.server.zones import initForCore
    except ImportError: pass
    else: initForCore()

    from stuphmud.server.player.commands import installCommands
    installCommands()


def installSystemConfig():
    from os import getenv
    config = getenv('STUPHOS_CONFIG')
    if config:
        reloadConfigFile(config)


# Event Bridge.
def bootStart():
    # Note: this function must return the bridge, or
    # the rest of the extension is not installed.

    # todo: import more of management
    # import mud.tools.debug

    installSystemConfig()

    bridge = installBridge()

    from stuphos.runtime.registry import getRegistry
    thisModule = getMudModule()
    getRegistry(create = thisModule.on) # Binding passed for shutdown-game registration.


    installSite()

    try:
        installServices(thisModule)
        installWorld()

        from stuphos.management.reboot import StartRecovery
        StartRecovery()

    except:
        logException(traceback = True)
    finally:
        return bridge

def bootComplete(timing):
    (secs, usecs) = timing
    from stuphos.management.reboot import CompleteRecovery
    CompleteRecovery()
