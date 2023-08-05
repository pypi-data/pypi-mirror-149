# MUD Tools.

# Tool Primitives.
def registerBuiltin(object, name = None):
    if name is None:
        name = object.__name__

    __builtins__[name] = object

def asBuiltin(function):
    registerBuiltin(function)
    return function

registerBuiltin(asBuiltin)


# System Tools.
import types

from os.path import basename, join as joinpath, dirname, normpath, abspath, splitext
from time import time as getCurrentSystemTime

import linecache
from linecache import getline as getLineFromCache, clearcache as clearLineCache, checkcache as checkLineCache
from linecache import getline

try: from json import load as fromJsonFile, loads as fromJsonString, dump as toJsonFile, dumps as toJsonString
except ImportError:
    try: from simplejson import load as fromJsonFile, loads as fromJsonString, dump as toJsonFile, dumps as toJsonString
    except ImportError:
        def jsonNotAvailable(*args, **kwd):
            raise NotImplementedError('Json methods not installed!')

        fromJsonFile = fromJsonString = toJsonFile = toJsonString = jsonNotAvailable

try: from collections import OrderedDict as ordereddict
except ImportError:
    # Provide our own implementation for < 2.7
    from .collections_hack import OrderedDict as ordereddict

from _thread import start_new_thread as _nth
def nth(function, *args, **kwd):
    return _nth(function, args, kwd)

# Also found in runtime.architecture.routines
def apply(function, *args, **kwd):
    return function(*args, **kwd)

asBuiltin(apply)


# Sub-tools.
from .debugging import breakOn, traceOn, remoteBreak, remoteTrace
from .debugging import enter_debugger, debugCall, debugCall as runcall
asBuiltin(breakOn)
asBuiltin(traceOn)
asBuiltin(remoteBreak)
asBuiltin(remoteTrace)
registerBuiltin(enter_debugger, 'debugOn')

from .errors import *
from .strings import *
from . import misc
from .misc import *
from .logs import *
from .cmdln import *

from . import timing

setupSubmodule(vars(), '.hashlib', 'hashlib',
               ('new', 'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'))

# Pygments.
try: from .pyg_colorizer import stuphColorFormat
except (SyntaxError, ImportError) as e:
    # print e
    pyg_colorizer = False

    def stuphColorFormat(string):
        # Identity.
        return string
