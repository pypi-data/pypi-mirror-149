# MUD Runtime -- Object Entities.
#
from .. import Concretion, declareEventController, EventController

# from types import DictionaryType
DictionaryType = dict
# from new import classobj as newClassObject
from types import new_class

def populateNamespace(data):
    def doNamespacePopulate(ns):
        ns.update(data)
    return doNamespacePopulate

def newClassObject(name, bases, values):
    return new_class(name, bases, exec_body = populateNamespace(values))

# Overall identity constant.
class Undefined(object):
    def __repr__(self):
        return self.__class__.__name__
    __str__ = __unicode__ = __repr__

Undefined = Undefined()

# Design Pattern.
class Singleton(object):
    # This should be further specialized into 'Event' for runtime constructs.
    class Meta(type):
        def __new__(self, name, bases, values):
            cls = type.__new__(self, name, bases, values)
            if Singleton in bases:
                return cls

            ##    postvalues = {}
            ##    for name in values.keys():
            ##        if name in ['__module__', '__doc__']:
            ##            postvalues[name] = values[name]
            ##            del values[name]
            ##
            ##    inst = cls(name, **values)
            ##    inst.__dict__.update(postvalues)
            ##    return inst

            return cls(name, **values)

# Identity.
class Object(object):
    class _Meta:
        Attributes = []

        def __init__(self, *attributes, **kwd):
            self.Attributes = list(attributes) + list(kwd.items())

        @staticmethod
        def formatAttribute(instance, a, default = Undefined):
            def getAttribute(name):
                if callable(name):
                    return name(instance)

                if name.endswith('()'):
                    v = getattr(instance._Meta, name[:-2], default)
                    if callable(v):
                        return v(instance)
                else:
                    return getattr(instance, name, default)

                return Undefined

            if type(a) in (list, tuple):
                if len(a) == 2:
                    return '%s = %r' % (a[0], getAttribute(a[1]))
                if len(a) == 3:
                    return '%s = %r' % (a[0], getAttribute(a[1], a[2]))

            elif type(a) is str:
                return '%s = %r' % (a, getAttribute(a))

        @staticmethod
        def className(instance):
            return instance.__object_name__()

        @classmethod
        def instanceRepr(self, instance):
            meta = instance._Meta
            attribs = ', '.join(meta.formatAttribute(instance, a) for \
                                a in meta.Attributes)
            if attribs:
                return '<%s %s>' % (meta.className(instance), attribs)

            return '<%s>' % meta.className(instance)

    def __init__(self, name = Undefined):
        if name is not Undefined:
            self.__name = name

    def __repr__(self):
        return self._Meta.instanceRepr(self)
    def __str__(self):
        return self.__repr__()

    # This should go in the Meta.
    def __object_name__(self):
        try: return self.__name
        except AttributeError:
            return self.__class__.__name__

    @classmethod
    def instanceOf(self, other):
        return isinstance(other, self)

        ##    try: return issubclass(other.__class__, self)
        ##    except AttributeError:
        ##        return False

from .lookup import LookupObject
LookupClassObject = LookupObject

class Synthetic(Object, dict): # todo: determine if adding dict base type is stable
    class _Meta(Object._Meta):
        Attributes = Object._Meta.Attributes + ['members()']

        @staticmethod
        def members(instance):
            return ', '.join(map(str, list(instance.__dict__.keys())))

    def __init__(self, dict = None, **values):
        if not isinstance(dict, DictionaryType):
            assert dict is None
            dict = values
        else:
            dict.update(values)

        self.__dict__ = dict

    # todo: FromStructure and ToStructure methods like in WRLC

class Namespace(Synthetic):
    # XXX namespace traditionally has a dict pointing to self.
    pass

namespace = Namespace


# Component Event Model.
# todo: rename to `Instrument'
# todo: make Singleton behavior part of new, AutoInstrument class.
class Component(Singleton, Concretion, metaclass=Singleton.Meta):
    # Todo: Rename to Instrument?
    '''
    class Me(Component):
        implements = EVENTS + ['movementXYZ']

        class Module:
            pass

            '''

    Module = 'bridge'

    def __init__(self, name, Module = None, **others):
        # Register this component class instance with bridge module.
        self.Target = others.get('Target', self)

        if Module is None:
            Module = self.Module

        self.bindToRuntime(Module) # system-dependent

        try: init = self.__instance_init__
        except AttributeError: pass
        else: init() # others['__init_args__']

    def __call__(self, ctlr, *args, **kwd):
        method = self.getTriggerFunction(ctlr.event_name)
        if callable(method):
            return method(ctlr, *args, **kwd)

    def __eq__(self, other):
        if self.sameClass(other):
            try:
                return self.__class__.__module__ == \
                         other.__class__.__module__ and \
                       self.__class__.__name__ == \
                         other.__class__.__name__

            except AttributeError:
                return False

    def getTriggerFunction(self, event_name):
        return getattr(self.Target, self.getTriggerName(event_name), None)
    def getTriggerName(self, event_name):
        return getTriggerName(event_name)

    def getEventNames(self, module):
        from ..events import getEventNames
        return getEventNames(module)


    DYNAMIC_TRIGGERS = False
    def bindToRuntime(self, Module = None):
        # system-dependent
        # Module: ExtensionPoint

        from ..events import Binding

        if Module == 'bridge':
            from stuphos import getBridgeModule
            Module = getBridgeModule()

        binding = Binding(Module)
        self.boundControllers = []

        for event in self.getEventNames(Module):
            # What this is saying is that it won't bind to events that don't exist.
            if self.DYNAMIC_TRIGGERS or callable(self.getTriggerFunction(event)):
                ctlr = binding.getController(event)
                ctlr.registerHandler(self)
                self.boundControllers.append(ctlr)

    def __repr__(self):
        return '%s.%s (Component)' % (self.__module__, self.__class__.__name__)

    def __registry_delete__(self):
        for ctlr in self.boundControllers:
            ctlr.unregisterHandler(self)


def getTriggerName(event_name):
    return 'on%s%s' % (event_name[0].upper(), event_name[1:])

def newComponent(cls, name = None, **values):
    if name is None:
        # Unfortunately, it ends up taking up the module name that calls newClassObject.
        name = '%s.%s' % (cls.__module__, cls.__name__)

    # values['__instance_init__'] = cls.__init__
    # values['__init_args__'] = (args, kwd)
    return newClassObject(name, (Component, cls), values)

# This should be in events, but it relies on Singleton.
class DeclareEvent(Singleton, metaclass=Singleton.Meta):
    def __new__(self, *args, **kwd):
        return declareEventController(*args, **kwd)


# Memory management.
class writable(object):
    # Base class for emulated object attribute sets.
    def _setAttribute(self, name, value):
        return object.__setattr__(self, name, value)

class representable:
    def __repr__(self):
        return '<%s>' % self.__class__.__name__

class writeprotected(writable, representable):
    # The preferred native object base class for constraining memory sets.
    # The reason is derives from representable is so that you don't have to
    # derive from both of them.

    def __setattr__(self, name, value):
        # Note: allowing all private sets (preceeding undescore) simplifies Pythonic
        # private variables becoming writable.  Now this becomes unsuitable for any-
        # thing other than expressing objects into the virtual environment (where private
        # members are already protected).

        # try: pub = getattr(self, "__public_members__", "nothing")
        # except Exception as e:
        #     pub = f'{e.__class__.__name__}: {e}'
        # else:
        #     if pub == 'nothing' and name == '_owner': # Our case.
        #         debugOn()

        # print(f'{name} in {pub}')

        if name.startswith('_') or name in getattr(self, '__public_members__', []):
            return self._setAttribute(name, value)

        raise AttributeError('Unwritable: %s' % name)

blockSetAttr = writeprotected

def getMemberStored(object, name):
    try: return object.__dict__[name]
    except KeyError:
        raise AttributeError(name)

class baseInstance(writable):
    def __setattr__(self, name, object):
        # from world import heartbeat as vm
        # task = vm.contextObject.task
        from stuphos.kernel import vmCurrentTask
        task = vmCurrentTask()

        try: existing = getMemberStored(self, name)
        except AttributeError:
            task.addObject(name)
        else:
            task.removeObject(existing)

        task.addObject(object)
        return self._setAttribute(name, object)


class extension:
    def __init__(self, object):
        self._object = object

wrapper = extension

def reprWrapper(self):
    return '<%s: type %s>' % (self.__class__.__name__,
                              self._object.__class__.__name__)

class extensionObject(writeprotected, Object, wrapper):
    # More opaque than a transparent object.
    __init__ = extension.__init__
    __repr__ = reprWrapper

    def _getExtensionOrObjectAttr(self, name):
        '''
        class remoteLibraryNativeExtension(extensionObject):
            """
            tool.remote-library:
                path: com/runphase/library-extension
                methods:
                    - object: stuphos.runtime.architecture.remoteLibraryNativeExtension._Install
                      name: remote

            interface:
                commands:
                    remoteInstall($method)::
                        def call(routine, args):
                            'com/runphase/library-extension/remote'()
                            return act(routine, args)

                        task = task$(call, $.components.object, args$())
                        return task.result()

                        """

            # Optionally:
            __getattr__ = extensionObject._getExtensionOrObjectAttr

            @classmethod
            def _Install(self, frame):
                # Do this once.
                task = frame.task
                task.native = self(task.native)

            def create(self, frame, path, *args):
                return log.library.create(path, *args) # *map(convertValue, args)

                '''

        try: return object.__getattribute__(self, name)
        except AttributeError:
            return getattr(self._object, name)


class Transparent(extensionObject):
    # Maybe translucent.
    pass

_transparent = Transparent

class ExceptionType(extensionObject):
    pass

class baseExceptionValue(extensionObject):
    pass

class safeNative(writeprotected):
    def __init__(self, callable):
        # self.__call__ = callable
        self._callable = callable
    def __call__(self, *args, **kwd):
        return self.__dict__['_callable'](*args, **kwd)

    def __getattr__(self, name):
        return getattr(self.__dict__['_callable'], name)

    # I don't know why I resort to this translation.  What am I hiding?
    # def __getattr__(self, name):
    #     # debugOn()
    #     try: return self.__dict__['_callable'][name] # translation
    #     except (TypeError, KeyError):
    #         raise AttributeError(name)

    def __getitem__(self, item):
        return self.__dict__['_callable'][item]

    def __repr__(self):
        return f'<native {self.__name__}>' # repr(self._callable)

    @property
    def __name__(self):
        # print(f"safe-native: {self.__dict__['_callable']}")
        return self.__dict__['_callable'].__name__

    @property
    def __doc__(self):
        # print(f"safe-native: {self.__dict__['_callable']}")
        return self.__dict__['_callable'].__doc__

_safe = _safe_native = safeNative

class safeNativeClass(object):
    def __getattribute__(self, name):
        o = object.__getattribute__(self, name)
        if callable(o):
            return _safe_native(o)

        return o

_safe_native_class = safeNativeClass

class safeNativeObject:
    def __init__(self, object):
        self._object = object

    # getattribute is required, but it catches .__dict__ (and probably .__class__)
    def __getattribute__(self, name):
        # print(f'safe-native.getattr: {name}')
        # debugOn()

        if name in ['__dict__', '__class__', '_object']:
            return object.__getattribute__(self, name)

        o = getattr(object.__getattribute__(self, '__dict__')['_object'], name)
        if callable(o):
            return _safe_native(o)

        return o

    def __repr__(self):
        try: name = self._object.__name__
        except AttributeError:
            name = self._object.__class__.__name__

        return f'<native-object {name}>'

    def __iter__(self):
        return self._object.__iter__()
    def __next__(self):
        return self._object.__next__()

_safe_native_object = safeNativeObject


class safeIterator(writeprotected):
    __init__ = safeNativeObject.__init__
    __repr__ = safeNativeObject.__repr__

    def __iter__(self):
        return iter(self._object)

    @classmethod
    def decorator(self, function):
        def call(*args, **kwd):
            return self(function(*args, **kwd))
        return call

_safe_iterator = safeIterator


# Execution Primitives.
class Procedure(Object):
    class Done(Exception, Object):
        pass

    # Note: This should probably define __call__ -> run(),
    # since that what a procedure does, which would simplify
    # heartbeat/engine code.

    class Interface(writeprotected, Object):
        # Revealed to the GIRL object runtime, proxies the local subroutine def
        # through the vm invocation instruction.
        class _Meta(Object._Meta):
            Attributes = [('procedure', lambda i: repr(i._procedure))]

        def __init__(self, procedure):
            self._procedure = procedure

        @property
        def _activation(self):
            # Return a copy of a PC-tracking invocation object.
            # Todo: Invocation(self._procedure)
            return self._procedure

    def __resolve__(self):
        return repr(self)


class Computer:
    # Instruction set.
    pass

class Source:
    pass


# Game-Level Objects.
class UnknownFlag(NameError):
    pass

class Bitvector(Object):
    # A pure implementation of the bitvector type in game module.
    class _Meta(Object._Meta):
        Attributes = Object._Meta.Attributes + ['set']

    def __init_subclass__(self, **kwd):
        pass

    def __init__(self, __bitv = 0, **bits):
        # This is an abstract base class.
        assert self.__class__ is not Bitvector

        self.__bitv = int(__bitv)
        for (name, value) in bits.items():
            setattr(self, name, bool(value))

        self.getUpperBitvNames()

    @classmethod
    def getUpperBitvNames(self):
        try: return self.__UPPER_BITVECTOR_NAMES
        except AttributeError:
            names = self.__UPPER_BITVECTOR_NAMES = \
                [n.upper() for n in self.BITVECTOR_NAMES]

        return names

    BITVECTOR_NAMES = []

    def isBitSet(self, bit):
        return bool(self.__bitv & bit)
    def getFlagBit(self, name):
        try: return (1 << self.getUpperBitvNames().index(name.upper()))
        except ValueError:
            raise UnknownFlag

    def isFlagSet(self, name):
        return self.isBitSet(self.getFlagBit(name))

    @property
    def names(self):
        return self.BITVECTOR_NAMES

    @property
    def set(self):
        return [name for name in self.names if self.isFlagSet(name)]

    @property
    def notset(self):
        return [name for name in self.names if not self.isFlagSet(name)]

    unset = nonset = notset

    def __getattr__(self, name):
        try: return self.isFlagSet(name)
        except UnknownFlag:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        try: bit = self.getFlagBit(name)
        except UnknownFlag: return object.__setattr__(self, name, value)
        else: self.__bitv |= bit if value else ~bit

    def __int__(self):
        return int(self.__bitv)
    def __str__(self):
        return ', '.join(map(str, self.set))
    def __iter__(self):
        return iter(self.set)

class PromptPreferences(Bitvector):
    BITVECTOR_NAMES = ['Mail', 'DataRate']
