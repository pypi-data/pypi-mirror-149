# Required for Command Dispatch:
from stuphmud.server.player import ACMD, HandleCommandError, PlayerAlert, playerAlert
from stuphos.etc.tools import getSystemException, stuphColorFormat
from stuphos.runtime.registry import getObject, registerObject, ObjectAlreadyRegistered

# Control-Point Support:
from stuphos.etc.tools import clearLineCache

from stuphmud.server.zones.specials import LookupSpecialObject
from stuphos import getConfig

import world
from world.unstructured import setWeather
import imp

def apply(function, *args, **kwd):
    return function(*args, **kwd)

def reloadModule(name):
    return imp.reload(__import__(name, globals(), locals(), ['']))

def parameters(min, max = None, doc = None):
    def makeParameterized(function):
        function.nParameters = (min, max)
        function.wizDoc = doc
        return function
    return makeParameterized

def paramArgstr(function):
    function.paramsArgstr = True
    return function

def parameterized_method(min, max = None, doc = None):
    def makeParameterized(function):
        def parameterizedMethod(self, *args, **kwd):
            return function(*args, **kwd)

        try: parameterizedMethod.__name__ = function.__name__
        except AttributeError: pass

        parameterizedMethod.nParameters = (min, max)
        parameterizedMethod.wizDoc = doc
        return parameterizedMethod
    return makeParameterized

def uncontrollable(function):
    function._uncontrollable = True
    return function

@apply
class ControlPoints:
    class Cancel(Exception):
        pass

    @parameters(1, 3)
    def set(self, peer, feature, attribute = None, value = None):
        feature = feature.lower()
        if feature == 'weather':
            attribute = attribute.lower() if attribute else ''
            if attribute == 'pressure':
                value = max(960, min(1040, int(value)))
                setWeather('pressure', value)
                playerAlert('Weather pressure set to: %d' % value)

            elif attribute == 'sky':
                playerAlert('Not yet implemented!')
            else:
                playerAlert('Unknown weather-set option: %r' % attribute)

        elif not feature:
            raise self.Cancel
        else:
            playerAlert('Unknown set feature: %r' % feature)

    # Should be part of system:
    @parameters(None)
    def clear_cache(self, peer):
        clearLineCache()
        playerAlert('Line-cache cleared!')

    @parameters(0)
    def load(self, peer, *modules):
        # Put them in the main namespace.
        import __main__ as main
        main = main.__dict__

        for m in modules:
            name = m.split('.')[0]
            try: main[name] = __import__(m)
            except ImportError:
                HandleCommandError(peer, getSystemException())
            else:
                print('Loaded: %s' % m)

    @parameters(0)
    def reload(self, peer, *modules):
        if not modules:
            modules = [__name__]

        modules = list(map(reloadModule, modules))
        clearLineCache()
        playerAlert('RELOADED:\r\n%s\r\n' % '\r\n'.join(map(str, modules)))

    @parameters(1)
    def reload_package(self, peer, package):
        # Delete all entries from the system modules that are under the
        # given package.  If the package-name is malformed, who cares.
        unloaded = self._unload_package(package)
        if unloaded:
            print('Unloaded:\n    %s' % '\n    '.join(unloaded), file=peer)
            print(file=peer)
        else:
            print('No submodules unloaded.', file=peer)

        # Then import the top-level.
        print('Reloading %s...' % package, file=peer)
        __import__(package)

    @parameters(0)
    def unload(self, peer, *packages):
        for p in packages:
            print('Unloaded:\n    %s' % \
                  '\n    '.join(self._unload_package(p)), file=peer)

    @uncontrollable
    def _unload_package(self, package):
        pGroup = package.split('.')
        pLength = len(pGroup)
        assert package # Not necessary, but we're paranoid.
        unloaded = []

        def isSubmodule(m):
            return m.split('.')[:pLength] == pGroup

        from sys import modules
        for m in filter(isSubmodule, iter(modules.keys())):
            unloaded.append(m)
            del modules[m]

        return unloaded

    @parameters(3, doc = 'Usage: assign {room|item|mobile} <vnum> <fully.qualified.module.Special>')
    def assign(self, peer, spec_type, vnum, fqName):
        player = peer.avatar
        if player is None:
            playerAlert('You must be connected to a player to use this command.')

        spec_type = spec_type.lower()
        if spec_type == 'room':
            if vnum == 'here':
                room = player.room
            elif vnum.isdigit():
                room = world.room(int(vnum))
            else:
                playerAlert('Usage: assign room <vnum | here> <name>')

            if room is None:
                playerAlert('Room not found: %r' % vnum)

            proc = LookupSpecialObject(fqName, spec_type = spec_type)
            if proc is not None:
                from stuphmud.server.zones.specials import SpecialManager
                SpecialManager.AssignRoom(room, proc)
                playerAlert('Installed %r into %r.' % (proc, room))
            else:
                playerAlert('Unknown procedure: %r' % fqName)

        elif spec_type == 'mobile':
            mobile = world.mobile(int(vnum)) if vnum.isdigit() else player.find(vnum)
            if mobile is None or not isinstance(mobile, world.mobile):
                playerAlert('Mobile not found: %r' % vnum)

            proc = LookupSpecialObject(fqName, spec_type = spec_type)
            if proc is not None:
                from stuphmud.server.zones.specials import SpecialManager
                SpecialManager.AssignMobile(mobile, proc)
                playerAlert('Installed %r into %r.' % (proc, mobile))
            else:
                playerAlert('Unknown procedure: %r' % fqName)

        elif spec_type == 'item':
            item = world.item(int(vnum)) if vnum.isdigit() else player.find(vnum)
            if item is None or not isinstance(item, world.item):
                playerAlert('Item not found: %r' % vnum)

            proc = LookupSpecialObject(fqName, spec_type = spec_type)
            if proc is not None:
                from stuphmud.server.zones.specials import SpecialManager
                SpecialManager.AssignMobile(item, proc)
                playerAlert('Installed %r into %r.' % (proc, item))
            else:
                playerAlert('Unknown procedure: %r' % fqName)

        else:
            playerAlert('Unknown special type: %r' % spec_type)

    @parameters(0, 2)
    def registry(self, peer, action = None, name = None):
        if action == 'delete':
            assert name
            from stuphos.runtime.registry import delObject
            delObject(name)

        elif action in (None, 'show'):
            from stuphos.runtime.registry import getRegistry
            from stuphos.etc.tools import maxWidth
            reg = getRegistry() # runtime_registry
            items = iter(reg.items())

            max_length = maxWidth((n for (n, v) in items), 10)
            fmt = '%%-%ds -- %%.%ds' % (max_length, max(40, 80 - max_length - 4))

            def escapeObjectRepr(v):
                return str(v).replace('\n', '\\n') # todo: use encode('string-escape')??

            # Sort ascending.
            items = list(reg.items())
            items.sort(lambda a, b:cmp(a[0], b[0]))
            peer.page_string('\r\n'.join(fmt % (n, escapeObjectRepr(v)) \
                                         for (n, v) in items) + '\r\n')

    def remote_debug(self, peer, command):
        if command == 'break':
            from rpdb import Rdb
            Rdb().set_trace()

    def charm(self, peer):
        # -system-path register /cygdrive/c/Program+Files/JetBrains/PyCharm+1.1.1/helpers
        from pydev import pydevd
        pydevd.settrace('localhost', port=4448, stdoutToServer=True, stderrToServer=True)

    try:
        from .web_debug import doBreakOnUrl
        break_url = staticmethod(doBreakOnUrl)
    except ImportError:
        pass

    from stuphmud.server.player.interfaces.code import doManageShellEvaluators
    shell = staticmethod(doManageShellEvaluators)

    # todo: delegate more dynamically.
    # from .olc import doCompareWorld as compare_world
    # compare_world = staticmethod(compare_world)

    # from .xdebug import doXDebug as xdebug
    # xdebug = staticmethod(xdebug)

    # from .system import doSystemPathControl, doSystemModuleControl, doSystemCheckpointControl
    # system_path = staticmethod(doSystemPathControl)
    # system_modules = staticmethod(doSystemModuleControl)
    # system_checkpoint = staticmethod(doSystemCheckpointControl)

    # from .profiling import doProfileHeartbeat
    # profile_heartbeat = staticmethod(doProfileHeartbeat)

    @parameters(1)
    def view_code(self, peer, moduleName):
        # Or, lookup only modules/submodules in system already.
        m = __import__(moduleName, fromlist = ['']) # LookupObject?
        try: f = m.__file__
        except AttributeError: pass
        else:
            if f[-4:].lower() == '.pyc':
                f = f[:-1]
            if f[-3:].lower() == '.py':
                code = open(f).read()
                code = stuphColorFormat(code)

                peer.page_string(code)

    @parameters(1, 3)
    def upload_zone(self, peer, vnum, database = 'primary', vnum2 = None):
        # Just transfer zone entry info from programmed archives setting to specified database.
        # STUPHLIB -> ORM
        showAvailable = False
        showDetails = False
        if vnum in ['--available', '--index']:
            showAvailable = True
        elif vnum in ['--details']:
            showDetails = True
        else:
            vnum = int(vnum)

        from stuphlib import wldlib, dblib
        world_path = getConfig('world-path', 'MUD')
        base = dblib.LocalIndex(world_path)

        w = wldlib.World(base)
        w.loadFromZoneIndex(cascade = False)

        if showDetails:
            if database == '--mobile':
                vnum2 = int(vnum2)
                zone = w.loadZone(vnum2 // 100)

                for mob in zone.mobiles:
                    if mob.vnum == vnum2:
                        def report():
                            yield '[#%8d] %s' % (mob.vnum, mob.shortdescr)
                            yield 'Keywords: &y%s&N' % mob.name
                            yield 'Long Description:'
                            yield '&y%s&N' % mob.longdescr
                            yield 'Description:'
                            yield '&y%s&N' % mob.descr
                            yield 'Flags: &y%s&N Align: &y%s&N Level: &y%s&N Armor: &y%s&N' % \
                                  (mob.mobflags, mob.alignment, mob.level, mob.armorclass)
                            yield 'Max Hit: &y%5s&N Max Move: &y%5s&N Max Mana: &y%5s&N Hitroll: &y%s&N Damroll: &y%s&N' % \
                                  (mob.max_hit, mob.max_move, mob.max_mana, mob.hitroll, mob.damroll)
                            yield 'Damage Dice: &y%s&N Size Damage Dice: &y%s&N Gold: &y%s&N Exp: &y%s&N' % \
                                  (mob.damnodice, mob.damsizedice, mob.gold, mob.experience)
                            # position = int(mob.position), default_position = int(mob.default_pos),
                            yield 'Sex: 0 Walk Type: &y%s&N' % getattr(mob, 'movemessage', 0)
                            yield ''

                        peer.page_string('\r\n'.join(report()))
                        break

                return

            if database == '--room':
                vnum2 = int(vnum2)
                zone = w.loadZone(vnum2 // 100)

                for room in zone.rooms:
                    if room.vnum == vnum2:
                        def report():
                            yield '[#%8d] %s [&y%s&N/&y%s&N]' % (room.vnum, room.name, room.flags, room.sector)
                            yield '&y%s&N' % room.descr
                            yield ''

                            for (dirCode, exit) in room.exits.items():
                                yield '    %s -- #&y%s&N [&y%s&N/&Y%s&N]' % (dirCode, exit['room-link'],
                                                                             exit['flags'], exit['key'])
                                yield '    Keywords: &y%s&N' % exit['keyword']
                                yield '    &y%s&N' % exit['descr']

                            if room.exits:
                                yield ''

                        peer.page_string('\r\n'.join(report()))
                        break

                return

            database = int(database)
            zone = w.loadZone(database)

            def report():
                yield '%r:' % zone
                yield ''

                yield 'Rooms: vnum name #exits flags'
                for room in zone.rooms:
                    yield '    [#%8d] %-40.40s %4d %s' % (room.vnum, room.name,
                                                          len(room.exits),
                                                          room.flags)
                yield ''

                yield 'Items: vnum shortdescr type'
                for item in zone.items:
                    yield '    [#%8d] %-40.40s %-2d' % (item.vnum, item.shortdescr, item.type)
                yield ''

                yield 'Mobiles: vnum shortdescr level max_hit'
                for mob in zone.mobiles:
                    yield '    [#%8d] %-40.40s %-3s %-5s' % (mob.vnum, mob.shortdescr, mob.level, mob.max_hit)
                yield ''

            peer.page_string('\r\n'.join(report()))
            return

        #start = time.now()
        if showAvailable:
            def report():
                #loadTime = time.now() - start
                for zone in sorted(iter(w.zoneMap.items()), key = lambda z: z[0]):
                    # todo: filter out already-loaded zones.
                    yield '[#%-8d] %s' % (zone[0], zone[1].name)

                yield ''

            peer.page_string('\r\n'.join(report()))
            return

        zone = w.loadZone(vnum)
        # zone = w.lookupZone(vnum)

        # Calculate the real number (*!@#$) using the current world as index.
        # XXX This won't work for sequentially uploaded zones! (Just once)
        index = [z.vnum for z in world.iterent(world.zone)]
        index.append(vnum)
        index.sort() # ascending
        rnum = index.index(vnum)

        # Upload zone, room, object and mobile prototype info.
        # Todo: assert distinct
        from stuphos.management import db, orm
        import sqlobject.dberrors

        # Todo: Do in transaction.
        with db.dbCore.hubThread(database) as conn:
            z = orm.Zones(id = vnum,
                          name = zone.name, lifespan = zone.lifespan, age = 0,
                          bottom = 0, # zone.bottom,
                          top = zone.top, flags = zone.flags,
                          reset_mode = getattr(zone, 'reset-mode', 0),
                          continent = zone.continent)

            z.sync()

            for (i, (command, if_flag, args)) in enumerate(zone.commands):
                args = list(map(int, args))
                c = orm.ZoneCommands(znum = i, command = c, if_flag = if_flag,
                                     arg1 = args[0], arg2 = args[1], arg3 = args[2],
                                     line = '')

                c.sync()

            # XXX This demands a shift up for all zone rnums in the rooms table above this new zone.
            # update rooms set zone = zone + 1 where zone >= $rnum
            # using conn
            u = conn.getConnection().cursor()
            u.execute('update rooms set zone = zone + 1 where zone >= %d' % rnum)

            try:
                for room in zone.rooms:
                    r = orm.Rooms(zone = rnum, name = room.name, sector_type = room.sector,
                                  description = room.descr, flags = room.flags,
                                  light = 0, number = room.vnum)
                    r.sync()

                    # Todo: load extra descriptions.
            except sqlobject.dberrors.DuplicateEntryError:
                pass
            except Exception as e:
                print(e.__class__.__module__, e.__class__.__name__, e, file=peer)

            try:
                for room in zone.rooms:
                    for (dirCode, exit) in room.exits.items():
                        e = orm.RoomDirections(rnum = room.vnum, direction = dirCode,
                                               description = exit['descr'],
                                               keyword = exit['keyword'],
                                               exit_flags = exit['flags'],
                                               exit_key = exit['key'],
                                               exit_destination = exit['room-link'])
                        e.sync()
            except sqlobject.dberrors.DuplicateEntryError:
                pass
            except Exception as e:
                print(e.__class__.__module__, e.__class__.__name__, e, file=peer)

            try:
                for item in zone.items:
                    i = orm.ObjectPrototypes(number = item.vnum,
                                             flags = item.extraflags, name = item.name,
                                             description = item.longdescr,
                                             short_description = item.shortdescr,
                                             action_description = item.actiondescr,
                                             value1 = item.value1,
                                             value2 = item.value2,
                                             value3 = item.value3,
                                             value4 = item.value4,
                                             type = item.type,
                                             wear_flags = item.wearflags,
                                             extra_flags = 0, # item.extra_flags,
                                             anti_flags = item.antiflags,
                                             weight = item.weight,
                                             cost = item.cost,
                                             cost_per_day = 0, # item.cost_per_day,
                                             timer = getattr(item, 'timer', 0),
                                             trap = 0, # item.trap,
                                             bitvector = 0,
                                             spec_proc = '')

                    i.sync()
            except sqlobject.dberrors.DuplicateEntryError:
                pass
            except Exception as e:
                print(e.__class__.__module__, e.__class__.__name__, e, file=peer)

            try:
                for mob in zone.mobiles:
                    m = orm.MobPrototypes(id = mob.vnum, name = mob.name, short_desc = mob.shortdescr,
                                          long_desc = mob.longdescr, description = mob.descr,
                                          flags = mob.mobflags, affected_by = mob.affbits,
                                          alignment = int(mob.alignment),
                                          a_str = 11, # mob.strength,
                                          a_str_add = 11, # mob.strength_addition
                                          a_int = 11, # mob.intelligence
                                          a_wis = 11, # mob.wisdom
                                          a_dex = 11, # mob.dexterity
                                          a_con = 11, # mob.constitution
                                          a_cha = 11, # mob.charisma
                                          level = int(mob.level), hitroll = int(mob.hitroll),
                                          armor = int(mob.armorclass), max_hit = int(mob.max_hit),
                                          hit = 0, # mob.hit,
                                          max_move = int(mob.max_move),
                                          move = 0, # mob.move
                                          max_mana = int(mob.max_mana),
                                          mana = 0, # mob.mana
                                          damage_dice = int(mob.damnodice), damage_dice_faces = int(mob.damsizedice),
                                          damroll = int(mob.damroll), gold = int(mob.gold), exp = int(mob.experience),
                                          position = int(mob.position), default_position = int(mob.default_pos),
                                          sex = 0, # mob.sex
                                          chclass = 0, weight = 0, height = 0,
                                          walk_type = getattr(mob, 'movemessage', 0),
                                          attack_type = 0, # mob.attack_type,
                                          spec_proc = getattr(mob, 'specproc', ''))
                    m.sync()

            except sqlobject.dberrors.DuplicateEntryError:
                pass
            except Exception as e:
                print(e.__class__.__module__, e.__class__.__name__, e, file=peer)

            # todo: shops

            print('STUPHLIB[%s] -> ORM[%s]:' % (world_path, database), file=peer)
            print(repr(zone), file=peer)

    @parameters(1, 2)
    def delete_zone(self, peer, vnum, database = 'primary'):
        # Nuke an entry in the database.
        vnum = int(vnum)

        from stuphos.management import db, orm
        with db.dbCore.hubThread(database) as conn:
            for zone in orm.Zones.selectBy(id = vnum):
                print('Destroying', zone, file=peer)
                zone.destroySelf()

                # todo: destroy rooms, zone commands, object and mobile prototypes, shops.
                # delete from object_prototypes where number / 100 = 20

            # todo: decrease all zone rnums in Rooms table over this zone, using conn.
            u = conn.getConnection().cursor()
            #u.execute('update rooms set zone = zone - 1 where zone > %d' % rnum)

    @parameters(0, 1)
    def show_players(self, peer, database = 'primary'):
        from stuphos.management import db, orm
        from io import StringIO
        import csv

        COLFMT = '#%8s %-20.20s %-30.30s %-40.40s %3s %8s %10s %8s'

        with db.dbCore.hubThread(database) as conn:
            u = conn.getConnection().cursor()
            u.execute('select (id, name, email, host, level, gold, bank_gold, played) from players order by host')

            def report():
                yield COLFMT % ('ID #', 'Name', 'Email', 'Host', 'Lvl', 'Gold', 'Bank', 'Played')

                for row in u:
                    # Parse each row.
                    record = row[0]
                    # '(1144,Cal,calvindastud@hotmail.com,"",105,9979704,1050000000,1698413)'
                    if record[0] == '(' and record[-1] == ')':
                        record = record[1:-1]

                    ((id, name, email, host, level, gold, bank, played),) = csv.reader(StringIO(record))

                    yield COLFMT % (id, name, email, host, level, gold, bank, played)

                yield ''

            text = '\r\n'.join(report())

        peer.page_string(text)

def getMinimumLevel(cmd):
    return 115 # cmd.level

#@runtime.api
@apply
class API:
    NAME = 'Wizard::Control::API'
    REGISTRY = NAME + '::Registry'

    def registerControlPoint(self, name, function):
        self.getRegistry()[name] = function
    def unregisterControlPoint(self, name):
        del self.getRegistry()[name]

    def getRegistry(self):
        return getObject(self.REGISTRY, create = dict)
    def getRegistryObject(self):
        return self.RegistryObject(API.getRegistry())

    def register(self, name): # parameter_info
        # Decorator-Maker:
        def registerFunction(function):
            self.registerControlPoint(name, function)
            return function

        return registerFunction

    class RegistryObject:
        # HAck -- todo, unify this more.
        def __init__(self, d):
            self.__dict__ = d

    parameters = staticmethod(parameters)
    paramArgstr = staticmethod(paramArgstr)

try: registerObject(API.NAME, API)
except ObjectAlreadyRegistered:
    pass

@apply
class WizControllers:
    def __iter__(self):
        yield ControlPoints # Builtin
        yield API.getRegistryObject()

@ACMD('-')
def doWizControl(peer, cmd, argstr):
    if peer.avatar is not None and peer.avatar.level >= getMinimumLevel(cmd):
        args = argstr.split() if argstr else []
        if args:
            larg = args[0]
            if not larg.startswith('_'):
                i = larg.find(':')
                if i < 0:
                    name = larg
                    args = tuple(args[1:])
                else:
                    name = larg[:i]
                    args = (larg[i+1:],) + tuple(args[1:])

                name = name.lower().replace('-', '_')
                for wizctlr in WizControllers:
                    ctlpt = getattr(wizctlr, name, None)
                    if getattr(ctlpt, '_uncontrollable', False):
                        continue

                    try: params = ctlpt.nParameters
                    except AttributeError: pass
                    else:
                        n = len(args)
                        try:
                            if params[0] is None:
                                if n:
                                    playerAlert('%r takes no parameters.' % name)
                            elif n < params[0]:
                                playerAlert('%r takes at least %d parameters.' % (name, params[0]))
                            elif params[1] is not None and n > params[1]:
                                playerAlert('%r takes at most %d parameters.' % (name, params[1]))

                        except PlayerAlert as e:
                            doc = getattr(ctlpt, 'wizDoc', None)
                            if doc:
                                print(doc, file=peer)

                            e.deliver(peer)
                            return True

                    try: params = ctlpt.paramsArgstr
                    except AttributeError: pass
                    else:
                        if params:
                            args = [argstr]

                    if callable(ctlpt):
                        try: ctlpt(peer, *args)
                        except ControlPoints.Cancel: return False
                        except PlayerAlert as e: e.deliver(peer)
                        except: HandleCommandError(peer, full_traceback = False)

                        return True

# Command-Programming:
##    from mud.player import ACMDLN, Option, isFromSecureHost
##    @ACMDLN('.', Option('--verb-name'),
##                 Option('--simple', action = 'store_true'),
##                 Option('--structured', action = 'store_false', dest = 'simple'),
##                 Option('--notebook-page'))
##    def doProgramVerb(player, command):
##        # De/Generate command code.
##        if player.avatar is not None and player.avatar.supreme and isFromSecureHost(player):
##            subCmd = command.nextArg().lower()
##            if subCmd == 'program':
##                # Decide verb name.
##                verbCode = command.options.verb_name or command.nextArg()
##                if not verbCode:
##                    print >> player, command.help()
##                    return True
##
##                # Decide command type (simple or structured)
##                # No: always complex, currently (because of api)
##                ##    if command.options.simple:
##                ##        from mud.player import ACMD as newVerb
##                ##        parameters = 'player, '
##                ##    else:
##                ##        from mud.player import ACMDLN as newVerb
##                ##        parameters = 'player, command'
##
##                # Invoke lambda-programming api.
##                from mud.player.commands import programVerbCommand, BuiltCommandError
##
##                # Todo: allow specification of cmdln options, as prologue:
##                #
##                # [option-name]
##                # short: o
##                # type: str
##                # default: not much
##                # action: store
##                # dest: option
##                #
##                # [another-option]
##                # action: store-true
##                #
##                # if not command.options.another_option:
##                #    print >> player, command.options.option
##                #
##
##                name = command.options.notebook_page
##                if name:
##                    # Interface with notebook api.
##                    # nb = runtime.Player.Notebook.API.Open(player)
##                    nb = runtime[runtime.Player.Notebook.API.Open](player)
##
##                    try: page = nb.getPageContent(name)
##                    except KeyError:
##                        print >> player, 'No page named: %r' % name
##                    else:
##                        # Build and register command from notebook page.
##                        try: programVerbCommand(verbCode, 'python', page)
##                        except BuiltCommandError, build:
##                            print >> player, 'Declaring Code:\n    %s\n' % \
##                                     '\n    '.join(build.declaration.split('\n'))
##
##                            from mud.player import HandleCommandError
##                            HandleCommandError(player, (build.syntax.__class__,
##                                                        build.syntax,
##                                                        build.tb))
##                        else:
##                            # New command registered.
##                            print >> player, 'Built %r from notebook: %r' % (verbCode, name)
##
##                    return True
##
##                # Start interactive programming!.
##                from mud.player.editor import Edit
##                @Edit(player, '')
##                def programVerb(peer, content):
##                    # Build and compile function definition.
##                    if not content.strip():
##                        print >> peer, 'Programming aborted.'
##                    else:
##                        try: programVerbCommand(verb, 'python', content)
##                        except BuiltCommandError, build:
##                            print >> peer, 'Declaring Code:\n    %s\n' % \
##                                  '\n    '.join(build.declaration.split('\n'))
##
##                            from mud.player import HandleCommandError
##                            HandleCommandError(peer, (build.syntax.__class__,
##                                                      build.syntax,
##                                                      build.tb))
##                        else:
##                            # New command registered.
##                            print >> peer, 'Programmed %r' % verbCode
##
##                return True
##
##            elif subCmd == 'deprogram':
##                # Crude.
##                # Decide verb name.
##                verbCode = command.options.verb_name or command.nextArg()
##                if not verbCode:
##                    print >> player, command.help()
##                    return True
##
##                try: commands = player.interpreter.commands
##                except AttributeError:
##                    print >> player, 'Not configured for commands!'
##                else:
##                    # First find the command function as named.
##                    action = commands.lookup(verbCode)
##                    if not action:
##                        print >> player, 'Unknown command: %s' % verbCode
##                    else:
##                        # Invoke removal of action.
##                        commands.remove(action)
##                        print >> player, 'Command removed:', action
##
##                return True
