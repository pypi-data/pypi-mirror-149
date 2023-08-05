# Configuration Object Model.

# Paths.
from os.path import join as joinpath, normpath, dirname
import sys

try: from path import path as pathObject
except ImportError:
    pathObject = str

def getPlatformDrivePath(drive_letter):
    if sys.platform.startswith('cygwin'):
        return '/cygdrive/%s' % str(drive_letter).lower()
    if sys.platform.startswith('win32'):
        return '%s:\\' % str(drive_letter).upper()

    return '/%s' % str(drive_letter)

def getStandardDrivePath(drive_letter, *parts):
    return getStandardPath(getPlatformDrivePath(drive_letter), *parts)

def getStandardPath(*parts):
    return pathObject(normpath(joinpath(*parts)))

def getParentPath(path, level = 1):
    # Standardize?
    for x in range(level):
        path = dirname(path)

    return path

# Configuration Files.
from configparser import ConfigParser, DEFAULTSECT, NoOptionError, NoSectionError

def loadConfig(filename, defaults = None):
    config = ConfigParser(defaults = defaults)
    config.read([filename])
    return Configuration(config, filename)

class Configuration:
    class Section:
        def __init__(self, config, section = None, **vars):
            if section is not None and type(section) is not str:
                raise TypeError(type(section).__name__)

            self.config = config
            self.section = section or DEFAULTSECT
            self.vars = vars

        def get(self, name, default = None):
            try: return self.config._config.get(self.section, name, vars = self.vars)
            except (NoOptionError, NoSectionError): return default

        def options(self):
            return self.config.options(self.section)

        def __iter__(self):
            return iter(self.options())
        def __getitem__(self, name):
            return self.get(name) # ??? Should this throw error?
        def __repr__(self):
            return "<Section '%s:%s'>" % (self.config.filename, self.section)

        @property
        def data(self):
            return dict((n, self.get(n)) for n in self.options())

    class _addressor:
        # todo: rewrite this with attributable.
        class _section:
            def __init__(self, addressor, name):
                self._addressor = addressor
                self._section = name

            def __getattr__(self, option):
                try: return object.__getattribute__(self, option)
                except AttributeError:
                    option = option.replace('_', '-')
                    return self._addressor.getSectionOption \
                        (self._section, option)

        def __init__(self, config):
            self._config = config

        def __getattr__(self, name):
            try: return object.__getattribute__(self, name)
            except AttributeError:
                return self._section(self, name)

        def getSectionOption(self, section, option):
            return self._config.get(option, section)


    def __init__(self, config, filename = None):
        self._config = config
        self.filename = filename

    def get(self, name, section = None, vars = None):
        try: return self._config.get(section, name, vars = vars)
        except (NoOptionError, NoSectionError): pass

    def sections(self):
        return self._config.sections()
    def options(self, section = None):
        try: return self._config.options(section or DEFAULTSECT)
        except NoSectionError: return []

    def getSection(self, section = None, **vars):
        return self.Section(self, section, **vars)
    def getDefaultSection(self, **vars):
        return self.getSection(self, **vars)

    def __iter__(self):
        return iter(self.sections())
    def __getitem__(self, section):
        return self.getSection(section)
    def __repr__(self):
        return "<Configuration '%s'>" % self.filename

    @property
    def addressor(self):
        return self._addressor(self)


# Package Support.
class PackageManager:
    def __init__(self, site_path = None, *components):
        if site_path is None:
            raise ValueError('Unsupported Site Path')

        self.site_path = site_path
        self.component_files = list(components)

    def install(self):
        from site import addpackage
        from sys import path as known_paths

        known_paths = set(known_paths)
        for comp_fl in self.component_files:
            # print(f'[addpackage] {self.site_path} / {comp_fl}')
            addpackage(self.site_path, comp_fl, known_paths)

# Standard MUD Properties.
LIB_ETC = getStandardPath('etc')
