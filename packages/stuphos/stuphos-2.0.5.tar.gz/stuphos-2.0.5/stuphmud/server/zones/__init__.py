# Zone-level records and object representation.
from stuphos import log, getConfig
from stuphos.runtime import Object
from stuphos.etc.tools import InterpolateStringVariables
from stuphos.etc.tools.logs import logException
from os.path import realpath, dirname, basename
from contextlib import contextmanager

from stuphos.kernel import Girl, Script

#girlSystemModule = runtime.Girl.System.Module

core = None
def initForCore():
    # Dynamically install component.
    from stuphos.runtime import Component
    class Instrument(Component, World):
        pass

    global core
    core = Instrument

    ##    global core
    ##    from mud.runtime import newComponent
    ##    core = newComponent(World)

class ZoneResetScript(Script):
    pass

# Top-Level Construct.
class World:
    ZONE_CONFIG_FILE = 'etc/zones.cfg'
    def getZoneConfigFile(self):
        return getConfig('zone-config-file') or self.ZONE_CONFIG_FILE

    from stuphmud.server.adapters import ZoneResetAccess

    def onResetStart(self, ctlr):
        self.zoneModules = loadZoneFile(self.getZoneConfigFile())

        # Import zone module associations.
        for module in self.zoneModules:
            try: module.importModule()
            except ImportError:
                name = module.name and ('[%s]' % module.name) or ''
                log('Unknown Zone Module%s: %r' % (name, module.package))


        # Initialize zone module associations.
        for module in self.zoneModules:
            # Configure special procedures first (that they may be overridden by module).
            # XXX Catch errors -- or, do this from within the loadSpecials routine.
            loadSpecialsConfigFromFile(module.getSpecialsFilename(self.getZoneConfigFile()))

            # Load module.
            loader = module.getLoader()
            if callable(loader):
                for zone in module.zones:
                    handle = zone.findHandle()
                    if handle is not None:
                        try: loader(self, module, zone, handle)
                        except: logException(traceback = True)


        # Do this first, before resetting the world.
        try:
            loadResetPrograms()
            loadTriggers()
            loadPlanets(self) # the unnamed solar system

        except TypeError as e:
            # Ths operation did not successfully complete.
            log('ERROR: %s' % (e,))


    # Supplemental.
    def onCreateZone(self, ctlr, zone):
        pass
    def onLoadZone(self, ctlr, zone):
        pass
    def onSaveZone(self, ctlr, zone):
        pass
    def onUnloadZone(self, ctlr, zone):
        pass

    def onStartZoneReset(self, ctlr, zone):
        from stuphos.kernel import GirlSystemModule

        try: program = zone.reset_program
        except AttributeError: pass
        else:
            if program is not None:
                script = program.module # Todo: Invocation(program.module)?

                from world import heartbeat as vm
                task = ZoneResetScript()
                task.environ.update(dict(zone = self.ZoneResetAccess._Get(zone)))
                                         # system = GirlSystemModule.Get()

                task.tracing = task.auditInstruction if program.tracing else None

                script.setEnvironment(task.environ)
                script.name = '#%d:%s' % (zone.vnum, zone.name)

                if program.programmer is None:
                    task += script
                else:
                    # import game
                    # game.syslog('zone-reset-programmer: %r' % program.programmer)
                    task.addFrameCall(script, programmer = program.programmer)

                vm += task

@contextmanager
def database():
    from stuphos.db import dbCore

    from stuphos import getConfig
    try:
        with dbCore.hubThread(getConfig('zone-database') or 'primary') as ctx:
            yield ctx

    except KeyError as e:
        # No known database by config key.
        raise TypeError('No database: %s' % (e,))


class ResetProgram:
    def __init__(self, zone, source, programmer = None, tracing = False):
        self.zone = zone
        self.source = source
        self.programmer = programmer
        self.tracing = tracing

        # zone.reset_program = self

    FLAG_AUDIT = (1 << 0)

    @property
    def module(self):
        return Girl(Girl.Module, self.source)

    @property
    def flags(self):
        yield dict(name = 'Audit', value = 'Audit', set = bool(self.tracing))

    @property
    def bitvector(self):
        return self.FLAG_AUDIT if self.tracing else 0

def loadResetPrograms():
    try:
        # Even though the db is sqlobject, WebProgrammer is a django-specific
        # component because, like zone reset input or OLC, it is web by design.
        #
        # In a strictly non-django runtime, this routine and the WebProgrammer 
        # object can be replaced by another source-specific impl.
        from stuphos.db.orm import ZoneResetProgram
        from phsite.network.embedded.olc.views import WebProgrammer

    except ImportError as e:
        print(f'[World Reset Programs] {e.__class__.__name__}: {e}')
    except Exception as e:
        print(f'[World Reset Programs] {e.__class__.__name__}: {e}')

    else:
        def load(zone):
            # debugOn()

            # todo: catch exception where there's no table programming error.
            # Q: Would it be any faster to select and iterate all db entities, and do world.zone BST lookups?
            for program in ZoneResetProgram.selectBy(zone = zone.vnum):
                # print(f'[reset.programs.load] {program.programmer}')
                zr = zone.reset_program = ResetProgram(zone, program.source.replace('\r', ''))
                if program.programmer in [None, '[None]', '']:
                    zr.programmer = None
                else:
                    zr.programmer = WebProgrammer(program.programmer)
                zr.tracing = bool((0 if program.flags is None else program.flags) & zr.FLAG_AUDIT)
                break
            else:
                pass

        import world
        with database():
            # debugOn()
            world.iterent(world.zone, load)

# from mud.tasks.triggers import loadTriggers, saveTrigger
def loadTriggers():
    from stuphos.triggers import getMobileTriggerTemplate
    from stuphos.kernel import Programmer
    import json
    try: from stuphos.db.orm import Triggers
    except ImportError:
        pass
    else:
        def load(zone):
            # Instantiate and configure a new trigger type by importing from database.
            for room in zone.rooms:
                for t in Triggers.selectBy(room = room.vnum):
                    break
            for item in zone.items:
                for t in Triggers.selectBy(item = item.vnum):
                    break
            for mobile in zone.mobiles:
                # Todo: select all triggers, iterate them matching internal world lookups.
                triggers = []
                for t in Triggers.selectBy(mobile = mobile.vnum):
                    template = getMobileTriggerTemplate(t.type)
                    data = json.loads(t.arguments) # list
                    progr = t.programmer
                    if progr == '[None]':
                        progr = None

                    trigger = template.CreateEmpty()
                    triggerType = template(trigger)

                    argsMap = triggerType.argumentsMapping()

                    for (nr, value) in enumerate(data): # ['arguments']):
                        argsMap[nr].setValue(trigger, value)

                    triggerType.setCode(t.program)
                    trigger.programmer = progr if progr is None else Programmer(progr)
                    trigger.tracing = trigger.FLAG_AUDIT & (0 if t.flags is None else t.flags)
                    triggers.append((t.number, trigger))

                # Bulk set import.
                triggers.sort(key = lambda t: t[0])
                mobile.triggers = [t[1] for t in triggers]

        import world
        with database():
            try: world.iterent(world.zone, load)
            except Exception as e: # ProgrammingError, e:
                import stuphos; stuphos.logException(traceback = True, header = 'World Load: %r' % e)


def saveTrigger(trigger, mobile = None, number = 0):
    # I/O
    from stuphos.triggers import MobileTrigger, getMobileTriggerType
    import json

    try: from stuphos.db.orm import Triggers
    except ImportError:
        return

    if isinstance(trigger, MobileTrigger):
        triggerType = getMobileTriggerType(trigger)
        args = [a.value for a in triggerType.arguments()]
        args = json.dumps(args)

        progr = trigger.programmer
        if progr is None:
            progr = '[None]'
        else:
            progr = progr.principal

        # Upsert.
        with database():
            for t in Triggers.selectBy(mobile = mobile.vnum, number = number):
                t.type = triggerType.typeCode
                t.arguments = args
                t.program = trigger.program
                t.programmer = progr
                t.flags = trigger.bitvector
                break
            else:
                #import pdb; pdb.set_trace()

                t = Triggers(mobile = mobile.vnum, number = number,
                             room = -1, item = -1, type = triggerType.typeCode,
                             arguments = args, program = trigger.program,
                             programmer = progr, flags = trigger.bitvector)

            t.sync()

class Planet(Object, list):
    # Planet-centric root because the planet is the only thing you can walk around on.
    # Also, there's no nomenclature for the solar system, galaxy or universe (yet).
    class _Meta(Object._Meta):
        Attributes = Object._Meta.Attributes + ['vnum', 'name', 'object']

    class Continent(Object, list):
        class _Meta(Object._Meta):
            Attributes = Object._Meta.Attributes + ['vnum', 'name', 'object']

        def __init__(self, planet, vnum, name = None, object = None):
            self.planet = planet
            self.vnum = vnum
            self.name = name
            self.object = object

        def library(self, task):
            from stuphos.kernel import Library
            core = runtime[runtime.Agent.System]
            return Library(task, core, core[self.object],
                           self.object)

        __rshift__ = library

        def addZone(self, zone):
            self.append(zone)
            return self
        __iadd__ = addZone

    def __init__(self, vnum, name = None, object = None):
        self.vnum = vnum
        self.name = name
        self.object = object

    def newContinent(self, vnum, name, object):
        c = self.Continent(self, vnum, name, object)
        self.append(c)
        return c

    def _enterSystem(self, core):
        self.system = core
        core.planets.append(self)

    def library(self, task):
        from stuphos.kernel import Library
        core = runtime[runtime.Agent.System]
        return Library(task, core, core[self.object],
                       self.object)

    __rshift__ = library

    # Todo: consider renaming to '_save'
    def save(self):
        try: from stuphos.db.orm import Planets, Continents
        except ImportError:
            return

        with database():
            vnum = self.vnum
            for p in Planets.selectBy(vnum = vnum):
                p.name = self.name
                p.object = self.object
                break
            else:
                p = Planets(vnum = vnum, name = self.name,
                            object = self.object)

            p.sync()
            for c in self:
                for o in Continents.selectBy(vnum = c.vnum):
                    o.name = c.name,
                    o.object = c.object
                    break
                else:
                    o = Continents(vnum = c.vnum, name = c.name,
                                   object = c.object,
                                   planet = vnum)
                o.sync()


def loadPlanets(core):
    core.planets = []

    try: from stuphos.db.orm import Planets, Continents
    except ImportError:
        return

    with database():
        # Planets.createTable()
        # Continents.createTable()

        for p in Planets.select():
            planet = Planet(p.vnum, p.name, p.object)
            for c in Continents.selectBy(planet = p.vnum):
                planet.newContinent(c.vnum, c.name, c.object)
                # Todo: implement this relation:
                # for z in c.zones:
                #     c.addZone(World.ZoneAccess(world.zone(z)))

            # The underscore here because a planet can be built using input data format (structure).
            planet._enterSystem(core)

def loadVerbCommands():
    pass


# Specials
from stuphmud.server.zones.specials import loadSpecialsConfigFromFile
from stuphmud.server.zones.specials import parseSpecialsConfigFromFile

from stuphmud.server.zones.config import dumpZoneInfoXMLToString
from stuphmud.server.zones.config import dumpZoneInfoConfigToString
from stuphmud.server.zones.config import dumpZoneModuleXMLToString
from stuphmud.server.zones.config import dumpZoneModuleConfigToString

DEFAULT_PATH_DIRECTORY = {'lib-etc': 'etc',
                          'lib-text': 'text',
                          'lib-misc': 'misc',
                          'lib-world': 'world'}

class ZoneModule:
    DEFAULT_ZONE_LOADER_NAME = '__load_zone__'

    class ZoneInfo:
        def __init__(self, nr, guid, name):
            self.nr = nr
            self.guid = guid
            self.name = name

        def findHandle(self):
            # TODO: Validate against guid and zname.
            import world # from game-module.

            try: return world.zone(self.nr)
            except ValueError: pass

        # Serialization.
        def getData(self):
            return (self.nr, self.guid, self.name)
        def toXMLString(self, indent = ''):
            return dumpZoneInfoXMLToString(self.getData(), indent = indent)
        def toConfigString(self):
            return dumpZoneInfoConfigToString(self.getData())

        __repr__ = __str__ = toXMLString

    def __init__(self, name, package, handler = None, specials = None):
        self.name = name
        self.package = package
        self.handler = handler
        self.specials = specials
        self.zones = []

    def importModule(self):
        if self.package:
            return __import__(self.package)

    def getPackage(self):
        # Rename to importPackage?
        # fromlist: must not be []
        # return __import__(self.package, globals(), locals(), [''])
        if self.package:
            try: return self._package
            except AttributeError: pass

            module = self.importModule()
            for m in self.package.split('.')[1:]:
                module = getattr(module, m)

            self._package = module
            return module

    def getHandlerName(self):
        return self.handler or self.DEFAULT_ZONE_LOADER_NAME
    def getLoader(self):
        try:
            package = self.getPackage()
            if package:
                return getattr(package, self.getHandlerName(), None)

        except ImportError:
            pass

    def getSpecialsFilename(self, zone_config_filename = None):
        values = DEFAULT_PATH_DIRECTORY.copy() # Also, from actual config variables..
        values['module-package-path'] = dirname(getattr(self.getPackage(), '__file__', ''))

        values['zone-config-path'] = realpath(dirname(zone_config_filename)) if zone_config_filename else ''
        values['zone-config-name'] = basename(zone_config_filename) if zone_config_filename else ''

        path = InterpolateStringVariables(self.specials, **values)
        # todo: convert to platform-specific path
        return path

    def loadSpecials(self, *args, **kwd):
        try: libdir = kwd.pop('libdir')
        except KeyError: libdir = None
        else: libdir = io.path(path) # XXX Unknown local 'path'

        path = self.getSpecialsFilename(*args, **kwd)
        if libdir is not None:
            path = libdir(path)

        return parseSpecialsConfigFromFile(path)

    loadedSpecials = property(loadSpecials)

    def addZone(self, nr, guid, zname):
        self.zones.append(self.ZoneInfo(nr, guid, zname))

    def __iadd__(self, info):
        self.addZone(*info)
        return self

    # Serialization.
    def getData(self):
        return (self.name, self.package, self.handler, self.getZoneData())
    def getZoneData(self):
        return dict((z.nr, z.getData()) for z in self.zones)
    def toXMLString(self, indent = ''):
        return dumpZoneModuleXMLToString(self.getData(), indent = indent)
    def toConfigString(self):
        return dumpZoneModuleConfigToString(self.getData())

    __repr__ = __str__ = toXMLString

def loadZoneModules(modules):
    zoneModules = []
    for (name, package, handler, specials, zones) in modules:
        zm = ZoneModule(name, package, handler = handler, specials = specials)
        for (nr, guid, zname) in zones.values():
            zm.addZone(nr, guid, zname)

        zoneModules.append(zm)
    return zoneModules

# Input Formats.
from .config import parseZoneConfigFromFile, parseZoneConfigFromString
from .config import parseZoneXMLFromFile, parseZoneXMLFromString
from .config import parseZoneJSONFromFile, parseZoneJSONFromString
from .config import parseZonePyFromFile, parseZonePyFromString

def loadZoneConfig(config):
    # XXX parseZoneConfig wasn't imported above
    return loadZoneModules(parseZoneConfig(config))

def loadZoneConfigFromFile(config_file):
    return loadZoneModules(parseZoneConfigFromFile(config_file))
def loadZoneConfigFromString(string):
    return loadZoneModules(parseZoneConfigFromString(string))

def loadZoneXMLFromFile(xml_file):
    return loadZoneModules(parseZoneXMLFromFile(xml_file))
def loadZoneXMLFromString(string):
    return loadZoneModules(parseZoneXMLFromString(string))

def loadZoneJSONFromFile(json_file):
    return loadZoneModules(parseZoneJSONFromFile(json_file))
def loadZoneJSONFromString(string):
    return loadZoneModules(parseZoneJSONFromString(string))

def loadZonePyFromFile(py_file):
    return loadZoneModules(parseZonePyFromFile(py_file))
def loadZonePyFromString(string):
    return loadZoneModules(parseZonePyFromString(string))

# YAML
# Pickle

# Generic.
from .config import parseZoneFile
def loadZoneFile(filename, *args, **kwd):
    return loadZoneModules(parseZoneFile(filename, *args, **kwd))


# Tracking.
def pathTo(origin, dest):
    from world import room as RoomType
    speedwalk = []
    while origin != dest:
        room = RoomType(origin)

        try: (dir, dist) = room.track(dest)
        except RuntimeError:
            break

        speedwalk.append(dir[0])
        origin = getattr(room, dir).room.vnum

    return speedwalk

def compressSpeedwalk(p):
    i = 0
    a = None
    for d in p:
        if a is None:
            a = d
            i = 1
        elif d != a:
            if i == 1:
                yield a
            else:
                yield '%d%s' % (i, a)

            a = d
            i = 1
        else:
            i += 1

    if a is not None:
        if i == 1:
            yield a
        else:
            yield '%d%s' % (i, a)

def speedwalk(origin, dest, compress = False):
    i = pathTo(origin, dest)
    if compress:
        i = compressSpeedwalk(i)

    return ''.join(i)
