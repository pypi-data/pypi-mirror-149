# World Library Comparison.
from _thread import start_new_thread as nth
from time import time as now
from datetime import datetime
from os.path import splitext, basename
from optparse import OptionParser
from pickle import load as unpickle, dump as pickle
from sys import exc_info

from stuphos import enqueueHeartbeatTask
from stuphos.etc.tools.timing import Elapsed
from stuphos.etc.tools import parseOptionsOverSystem
from stuphmud.server.player import HandleCommandError
from stuphmud.server.player.shell import PromptFor

from stuphlib.wldlib import World
from stuphlib.dblib import LocalIndex, ArchiveIndex, ZipArchiveIndex

from stuphmud.server.player.db.managedfs import getCheckedPlayerFilename, PERSONAL_PLRFILE_DIR
from .wizard import parameters

# Preparation.
def nowstr():
    return datetime.fromtimestamp(now()).strftime('%b%dth%Y')
def getDefaultOutputFilename(name):
    (name, ext) = splitext(name)
    return '%s-%s.txt' % (name, nowstr())

def sendToPeer(peer, message, inline = False):
    message = '&w%s&N' % message
    if inline:
        peer.sendln(message)
    else:
        enqueueHeartbeatTask(peer.sendln, message)

def getArchiveIndex(filename):
    (name, ext) = splitext(filename)
    if ext.lower() == '.zip':
        return ZipArchiveIndex(filename)

    raise TypeError(ext)

def LoadWorld(index):
    w = World(index)
    w.loadWorld(cascade = True)
    return w

# Interface.
def parseOptions(args):
    parser = OptionParser()
    parser.add_option('-o', '--output')
    parser.add_option('-g', '--debug', action = 'store_true')
    parser.add_option('-u', '--local-pickle', '--unpickle')
    parser.add_option('-p', '--pickle')

    parser.add_option('--no-info', action = 'store_false', default = True,
                      dest = 'info')
    parser.add_option('--no-commands', action = 'store_false', default = True,
                      dest = 'commands')
    parser.add_option('--no-rooms', action = 'store_false', default = True,
                      dest = 'rooms')
    parser.add_option('--no-items', action = 'store_false', default = True,
                      dest = 'items')
    parser.add_option('--no-mobiles', action = 'store_false', default = True,
                      dest = 'mobiles')

    return parseOptionsOverSystem(parser, args)

@parameters(1)
def doCompareWorld(peer, *options):
    (options, args) = parseOptions(options)
    if options.pickle:
        # Actually, just load the world and then pickle it.
        def convertLocalWorld(pickleFile):
            e = Elapsed()
            w = LoadWorld(LocalIndex('world'))
            sendToPeer(peer, 'Load Time: %s\r\nPickling...' % e, inline = True)
            nth(dumpWorldPickle, (w, pickleFile))

        def dumpWorldPickle(w, pickleFile):
            e = Elapsed()
            pickle(w, open(pickleFile, 'w'))
            sendToPeer(peer, 'Time: %s' % e)

        sendToPeer(peer, 'Loading local world...', inline = True)
        enqueueHeartbeatTask(convertLocalWorld, options.pickle)
        return

    name = args[0] # XXX assertion

    filename = getCheckedPlayerFilename(peer, name, PERSONAL_PLRFILE_DIR)
    playerArchive = getArchiveIndex(filename)
    outputfile = getCheckedPlayerFilename(peer, options.output or getDefaultOutputFilename(name),
                                          PERSONAL_PLRFILE_DIR)

    def comparatorThread(this):
        try:
            e = Elapsed()
            that = LoadWorld(playerArchive)
            sendToPeer(peer, 'Load Time: %s\r\nComparing...' % e)

            e = Elapsed()
            result = compareWorlds(this, that,
                                   info = options.info,
                                   commands = options.commands,
                                   rooms = options.rooms,
                                   items = options.items,
                                   mobiles = options.mobiles)

            # The comparison result and analysis is bundled together as text,
            # so the result is expected to be writable to file, just so.
            fl = open(outputfile, 'wt')
            fl.write(result)
            fl.close()

            sendToPeer(peer, ('Analysis Complete: %s\r\n' +
                              'Time: %s') % (basename(outputfile), e))

            def confirmView(peer, line):
                line = line.strip().lower()
                if line in ['y', 'ye', 'yes']:
                    peer.page_string(open(outputfile).read())

            enqueueHeartbeatTask(PromptFor, peer, confirmView, message = 'View? ')

        except:
            enqueueHeartbeatTask(HandleCommandError, peer, exc = exc_info())

    # The advantage of loading from pickle is (not speed, curiously, but) to
    # do so in another thread and not block the mud.
    sendToPeer(peer, 'Loading local world...', inline = True)
    if options.local_pickle:
        # Loading a pickle can be done in another thread, because it's not
        # really the active world (even though it's in the place of it).
        def loadPickleAndStartComparison(pickleFile):
            try:
                e = Elapsed()
                this = unpickle(open(pickleFile))

                sendToPeer(peer, 'Load Time: %s\r\nLoading %s...' % (e, basename(filename)))
                comparatorThread(this)
            except:
                enqueueHeartbeatTask(HandleCommandError, peer, exc = exc_info())

        nth(loadPickleAndStartComparison, (options.local_pickle,))
    else:
        def startComparison():
            # This should be done within the heartbeat to synchronize with active db ops.
            try:
                e = Elapsed()
                this = LoadWorld(LocalIndex('world'))

                sendToPeer(peer, 'Load Time: %s\r\nLoading %s...' % (e, basename(filename)), inline = True)
                nth(comparatorThread, (this,))
            except:
                HandleCommandError(peer)

        enqueueHeartbeatTask(startComparison)

# Algorithm:
# todo: proper zcommands and exits comparison.
# todo: analysis resulting in stuph:document format for olc web deployment.
ZONE_ATTRIBUTES = ('continent', 'flags', 'name', 'resetModeName', 'top')
ROOM_ATTRIBUTES = ('descr', 'flags', 'name', 'sectorName')
ITEM_ATTRIBUTES = ('actiondescr', 'antiflags', 'cost', 'extraflags', 'longdescr',
                   'minlevel', 'name', 'shortdescr', 'type', 'wearflags', 'weight',
                   'value1', 'value2', 'value3', 'value4')
MOBILE_ATTRIBUTES = ('affbits', 'alignment', 'armorclass', 'damnodice',
                     'damroll', 'damsizedice', 'default_pos', 'descr',
                     'experience', 'gender', 'gold', 'hitroll', 'level',
                     'longdescr', 'max_hit', 'max_mana', 'max_move',
                     'mobflags', 'name', 'position', 'shortdescr')

def compareWorlds(this, that, info = True, commands = True, rooms = True, items = True, mobiles = True):
    def compareZones(these, those):
        for (vnum, zone) in these.items():
            try: z = those[vnum]
            except KeyError:
                yield [['zone', vnum], 'removed']
            else:
                if info:
                    for attribute in ZONE_ATTRIBUTES:
                        value = getattr(z, attribute)
                        if value != getattr(zone, attribute):
                            yield [['zone', vnum], [attribute, value]]

                if commands:
                    # yield filterNone(compareCommands(zone.zcommands, z.zcommands))
                    yield filterNone(compareObjects(getattr(zone, 'commands', []),
                                                    getattr(z, 'commands', [])))

                if rooms:
                    yield filterNone(compareRooms(zone.roomMap, z.roomMap))
                if items:
                    yield filterNone(compareItems(zone.itemMap, z.itemMap))
                if mobiles:
                    yield filterNone(compareMobiles(zone.mobileMap, z.mobileMap))

        for (vnum, zone) in those.items():
            if vnum not in these:
                yield [['zone', vnum], 'added', getFullZoneData(zone)]

    def compareCommands(these, those):
        return compareObjects([(c.arg1, c.arg2, c.arg3, c.conditional) for c in these],
                              [(c.arg1, c.arg2, c.arg3, c.conditional) for c in those])

    def compareRooms(these, those):
        for (vnum, room) in these.items():
            try: r = those[vnum]
            except KeyError:
                yield [['room', vnum], 'removed']
            else:
                for attribute in ROOM_ATTRIBUTES:
                    value = getattr(r, attribute)
                    if value != getattr(room, attribute):
                        yield [['room', vnum], [attribute, value]]

                # Now, analyze .exitdirs

        for (vnum, room) in those.items():
            if vnum not in these:
                yield [['room', vnum], 'added', getFullRoomData(room)]

    def compareItems(these, those):
        for (vnum, item) in these.items():
            try: i = those[vnum]
            except KeyError:
                yield [['item', vnum], 'removed']
            else:
                for attribute in ITEM_ATTRIBUTES:
                    value = getattr(i, attribute)
                    if value != getattr(item, attribute):
                        yield [['item', vnum], [attribute, value]]

        for (vnum, item) in those.items():
            if vnum not in these:
                yield [['item', vnum], 'added', getFullItemData(item)]

    def compareMobiles(these, those):
        for (vnum, mob) in these.items():
            try: m = those[vnum]
            except KeyError:
                yield [['mobile', vnum], 'removed']
            else:
                for attribute in MOBILE_ATTRIBUTES:
                    value = getattr(m, attribute)
                    if value != getattr(mob, attribute):
                        yield [['mobile', vnum], [attribute, value]]

        for (vnum, mob) in those.items():
            if vnum not in these:
                yield [['mobile', vnum], 'added', getFullMobileData(mob)]

    # Resulting output format (yaml):
    from yaml import dump
    return dump(filterNone(compareZones(this.zoneMap, that.zoneMap)))

# For now, just return a summary for reference.
def getFullZoneData(zone):
    return repr(zone)
def getFullRoomData(room):
    return repr(room)
def getFullItemData(item):
    return repr(item)
def getFullMobileData(mob):
    return repr(mob)

# Generic Routines.
def filterNone(sequence):
    return [_f for _f in sequence if _f]

def compareObjects(this, that):
    from yaml import dump
    from os import popen, unlink
    from os.path import exists, join as joinpath
    from random import choice

    def getRandomFilename(tmppath = '/tmp', alphabet = 'abcdef0123'):
        while True:
            filename = ''.join(choice(alphabet) for x in range(10))
            filename = joinpath(tmppath, filename)
            if not exists(filename):
                return filename

    fn1 = getRandomFilename()
    fn2 = getRandomFilename()
    fn3 = getRandomFilename()

    try:
        fl = open(fn1, 'w')
        fl.write(dump(this))
        fl.close()

        fl = open(fn2, 'w')
        fl.write(dump(that))
        fl.close()

        popen('diff %r %r > %r' % (fn1, fn2, fn3))
        return open(fn3).read()

    finally:
        unlink(fn1)
        unlink(fn2)
        unlink(fn3)
