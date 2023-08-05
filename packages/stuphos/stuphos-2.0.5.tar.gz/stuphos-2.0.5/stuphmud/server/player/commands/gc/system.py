# System path, module and uptime checkpoint control.
# Copyright 2011 Clint Banis.  All rights reserved.
from stuphos.system.api import mudlog, syslog
from stuphos.etc.tools import maxWidth, columnize

import sys as system_module
from os.path import join as joinpath, isdir, exists, sep as ROOT_SEP, expanduser
from datetime import datetime
from time import time as getCurrentSystemTime

CYGDRIVE = ROOT_SEP + 'cygdrive'
def translateRoot(name):
    if len(name) == 1 and name.isalpha():
        return joinpath(CYGDRIVE, name)
    elif name in '~@':
        return expanduser('~')

    return name

def buildPath(*args):
    assert args
    return joinpath(translateRoot(args[0]), *args[1:])

def isZipArchive(path):
    # lame:
    return path.endswith('.zip') or path.endswith('.egg')

def getPathInfo(path):
    kind = ' '
    if isdir(path):
        kind = '+'
    elif exists(path):
        if isZipArchive(path):
            kind = 'Z'
    else:
        kind = '!'

    return '%s %s' % (kind, path)

def doSystemPathControl(peer, action = None, *args):
    if action == 'show' or not action:
        peer.page_string('\r\n'.join(map(getPathInfo, system_module.path)) + '\r\n')

    elif action == 'register':
        path = buildPath(*args)
        path = path.replace('+', ' ')
        if path in system_module.path:
            print('Already Registered: %s' % path, file=peer)
        else:
            system_module.path.append(path)
            print('Registered: %s' % path, file=peer)

    elif action == 'unregister':
        path = buildPath(*args)
        path = path.replace('+', ' ')
        if path in system_module.path:
            system_module.path.remove(path)
            print('Removed: %s' % path, file=peer)
        else:
            print('Not Registered: %s' % path, file=peer)

def doSystemModuleControl(peer):
    sysModules = system_module.modules
    modules = list(sysModules.keys())
    modules.sort()

    # Find all top-level module packages.
    toplevel = []
    for m in modules:
        for t in toplevel:
            if m.startswith(t):
                break
        else:
            toplevel.append(m)

    # Gather modules under their imported paths.
    builtins = []
    paths = {}
    from os.path import dirname, basename
    for t in toplevel:
        try: f = sysModules[t].__file__
        except AttributeError:
            builtins.append(t)
            continue

        if f is not None:
            if basename(f).startswith('__init__.'):
                # Trully is a package module: use the parent of parent.
                f = dirname(dirname(f))
            else:
                f = dirname(f)

            paths.setdefault(f, []).append(t)

    # Render display of them.
    def recolumnize(a, tab = '  ', min = 3, max = 20):
        return tab + ('\n' + tab).join(columnize(a, min, maxWidth(a, max)).split('\n'))
    def group(name, a):
        return '\n'.join([name + ':', (len(name) + 1) * '=', recolumnize(a)])

    s = []
    for p in system_module.path:
        m = paths.get(p)
        if m:
            s.append(group(p, m))

    if builtins:
        s.append(group('Builtin Modules', builtins))

    peer.page_string('\n\n'.join(s) + '\n')

# Checkpointing (Uptime Tracking).
# Todo: put into web.services, because it's not just command-oriented.
# The command stuff can be registered dynamically with the WizControl API.
DEFAULT_INTERVAL = (60 * 20, 0) # 20 Minutes
SYSTEM_CHECKPOINT_STATUS_NAME = 'System::Checkpointing::Status'
SYSTEM_CHECKPOINT_LAST_NAME = 'System::Checkpointing::LastTime'

from stuphos.runtime.registry import getObject, setObject
def isCheckpointingEnabled():
    return bool(getObject(SYSTEM_CHECKPOINT_STATUS_NAME))
def setCheckpointingEnabled(status = True):
    setObject(SYSTEM_CHECKPOINT_STATUS_NAME, bool(status))

def getLastCheckpoint():
    return getObject(SYSTEM_CHECKPOINT_LAST_NAME)
def setLastCheckpoint(value):
    setObject(SYSTEM_CHECKPOINT_LAST_NAME, value)

def systemCheckpoint():
    # Pings an outside system monitor to let it know we're still running.
    # Todo: do this in another thread, since web communication obviously takes time.accept2dyear
    # The event-queue can handle the callback of success or failure.
    # XXX Where is this?
    from stuphos.network.services import CheckpointUptime
    message = CheckpointUptime()
    if message:
        message = 'CHECKPOINT-ERROR: %s' % message
    else:
        message = 'SYSTEM: Uptime Checkpoint'
        setLastCheckpoint(getCurrentSystemTime())

    mudlog(message)
    syslog(message)

def systemCheckpointAdapter(sec, usec):
    systemCheckpoint()

forceSystemCheckpoint = systemCheckpoint

def EnableCheckpointing(interval = DEFAULT_INTERVAL):
    if not isCheckpointingEnabled():
        from world import heartbeat
        heartbeat.registerRealtimeAdapter(systemCheckpointAdapter, interval or DEFAULT_INTERVAL)
        setCheckpointingEnabled()
        return True

def DisableCheckpointing():
    if isCheckpointingEnabled():
        from world import heartbeat
        heartbeat.unregisterRealtimeAdapter(systemCheckpointAdapter)
        setCheckpointingEnabled(False)
        return True

def doSystemCheckpointControl(peer, action = 'show', interval = None):
    if action == 'show':
        print('Checkpointing %sactivated.' % ('' if isCheckpointingEnabled() else 'de'), file=peer)
        last = getLastCheckpoint()
        if last is not None:
            delta = datetime.fromtimestamp(getCurrentSystemTime()) - datetime.fromtimestamp(last)
            seconds = delta.seconds # total_seconds() -- version incompatibilities
            print('Last Checkpoint: %s ago' % seconds, file=peer) # days, seconds, microseconds
            # what about seconds to next??

    elif action == 'enable':
        print('Checkpointing %senabled.' % ('' if EnableCheckpointing(interval) else 'already '), file=peer)

    elif action == 'disable':
        print('Checkpointing %sdeactivated.' % ('' if DisableCheckpointing() else 'already '), file=peer)

    elif action == 'update':
        if isCheckpointingEnabled():
            forceSystemCheckpoint()
            print('Checkpoint forced.', file=peer)
        else:
            print('Checkpointing deactivated.', file=peer)

    else:
        print('Unknown system-checkpoint action: %r' % action, file=peer)
