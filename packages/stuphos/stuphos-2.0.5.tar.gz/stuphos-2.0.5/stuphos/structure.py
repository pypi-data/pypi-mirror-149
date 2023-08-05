# mud.management.structure

# XXX upgrade this to use lang.document.structural
# from op.runtime.structural.document import Submapping, Core
from stuphos.language.document.structural import Submapping, Core

from stuphos.runtime import Object
from stuphos.runtime.architecture.api import writeprotected, extension
from stuphos.etc.tools.strings import renderTemplate
from stuphos.etc.tools.logs import tracebackString, exceptionHeader
from stuphos.etc.tools import isYesValue
from stuphos.kernel import Subroutine, grammar, Girl, Script, executeGirl, newModuleTask
from stuphos.kernel import vmNewMapping, AutoMemoryMapping, AutoMemorySequence, Processor
from stuphos.kernel import vmNewSequence, vmCurrentTask, BypassReturn, MemorySequence
from stuphos.kernel import MemoryMapping, Instance, protectedMemoryLoad
from stuphos.kernel import constrainStructureMemory, TaskCreation
from stuphos import getConfig

from queue import Queue
import json, re


class MarshalizedObject(writeprotected, extension):
    def __init__(self, object):
        extension.__init__(self, json.dumps(object))
    def __call__(self):
        return protectedMemoryLoad(vmCurrentTask(), json.loads(self._object))


def convertTaskValue(task, value):
    if isinstance(value, MemorySequence):
        return task.sequence(convertTaskValue(task, i) for i in value)
    if isinstance(value, MemoryMapping):
        return task.mapping(*(convertTaskValue(task, i) for i in value.items()))
    if isinstance(value, Instance):
        return MarshalizedObject(value)

    return value

def vmConvertTaskValue(value):
    return convertTaskValue(vmCurrentTask(), value)

def outcomeOf(task, onComplete):
    c = vmCurrentTask()

    # todo: if self._task is currently not running,
    # then return self._task.stack[-1] immediately.

    c -= c.frame # this pure frame.

    s = c.machine.suspendedTasks
    s.suspendTask(c)

    @onComplete
    def complete(_, exception = None):
        # print(f'Task.result.complete: {exception}')

        if exception:
            (etype, value, tb) = exception
            s.resumeTask(c, c.machine, exception = value)

        else:
            # try: value = task.stack.pop()[0]
            try: value = task.stack[-1]
            except IndexError: value = None

            value = convertTaskValue(c, value)
            s.resumeTask(c, c.machine, value = value)

    raise BypassReturn

def getPrimaryIdentity(user):
    for default in user.default_players.all():
        return default.player.player_name


class Emulation(Script):
    # todo: override exception-handling, storing exception on task.
    # Then, read flag on (rendering) task completion handler
    # to know what to do (push q reponse) with it.

    debugging = False # True
    if debugging:
        def tracing(self, frame, pos, instr, args):
          # import pdb; pdb.set_trace()
          name = getattr(instr, '__name__', '?')
          msg = '%04d: %s(%s)' % (pos, name, ', '.join(map(repr, args)))

          # print(frame.procedure)
          print(msg)

          # if name == 'call':
          #     print '    %r' % frame.task.stack[-1]
          #     if frame.task.name:
          #         print '    %s' % frame.task.name


class EmulatedCodeTaskCreation(TaskCreation):
    def __init__(self, trigger, operator = None, audit = None, trace = None,
                 account = None, traceback = None, initialize = None, name = None,
                 timeout = None, finishingScript = None, *args, **kwd):

        TaskCreation.__init__(self, *args, **kwd)
        self.trigger = trigger

        self.operator = operator
        self.audit = audit
        self.trace = trace
        self.account = account
        self.traceback = traceback
        self.initialize = initialize
        self.name = name
        self.timeout = timeout
        self.finishingScript = finishingScript

    def createTask(self, environ):
        return self.taskClass.Load(environ = environ, user = self.user)

    def preInitTask(self, task, *args, **kwd):
        if self.operator is not None:
            task.operator = self.operator

        if self.audit == 'debug':
            task.tracing = task.__class__.debugInstruction
        elif self.audit is True:
            task.tracing = task.__class__.auditInstruction

        elif self.audit is None:
            if self.trace is not None:
                task.tracing = self.trace

        # For billing API.
        if self.account is not None:
            task.account = self.account

        self.procedure.setEnvironment(task.environ)

        return TaskCreation.preInitTask(self, task, *args, **kwd)


    def postInitTask(self, task, frame):
        if self.traceback is not None:
            try: runtime.call.System.Journal.waitLogs(task, self.traceback)
            except runtime.doesNotExist: pass

        if self.initialize:
            # A chance to construct memory-bound objects.
            # debugOn()
            self.initialize(task)

        if self.name is not None:
            task.name = self.name

        if self.timeout: # Is non-zero.
            self.applyTimeout(task, self.timeout)

        # todo: pass remaining kwd from _activate (synchronous).
        # TaskCreation.postInitTask(self, task, frame)
        executeGirl(task)

        if self.finishingScript:
            @task.onComplete
            def done(task, exception = None):
                # Spawn new task.
                newModuleTask(self.finishingScript, trigger = self,
                              completedTask = task)

        return task

    def applyTimeout(self, task, timeout):
        self.trigger.checkValidTimeout(timeout)

        from world import heartbeat as vm
        from stuphos.kernel import Pure
        from ph.interpreter.mental.native import _setTimeout # todo: get from stuphos.kernel

        def terminateTask():
            task.Terminate(task.machine)

        # environ['timeout$'] = \
        _setTimeout(vm, self.user,
                    self.programmer,
                    Pure(terminateTask),
                    timeout, None)


class Trigger(writeprotected, Object):
    # todo: get rid of synchronous attr, it has no meaning
    __public_members__ = ['code', 'environment']

    __name__ = 'trigger' # ?

    TIMEOUT_MAX = 60 * 60 * 24 * 7 * 4 * 3 # 3 Months.

    def __init__(self, code, synchronous = False, environment = None, path = None):
        self.code = code
        self._synchronous = synchronous
        self.environment = environment
        self._path = path

        # todo: on-construct security check for synchronous allowed.

    @property
    def synchronous(self):
        return self._synchronous

    @property
    def preprocessedCode(self):
        # Always a module -- account for single-line yaml.
        return self.code + '\n' # return renderTemplate(self.code, trigger = self)

    @property
    def _module(self):
        # try: return self._m_module
        # except AttributeError:
        #   from mud.lang.girl import Girl
        #   mod = self._m_module = Girl(Girl.Module, self.preprocessedCode)
        #   return mod
        return Girl(Girl.Module, self.preprocessedCode)

    @property
    def _expression(self):
        # How will this work with newlines?
        return Girl(Girl.Expression, self.preprocessedCode)

    _Emulation = Emulation


    def checkValidTimeout(self, timeout):
        # raise NotImplementedError

        if not isinstance(timeout, (int, float)):
            raise TypeError(type(timeout).__name__)

        if timeout <= 0 or timeout > self.TIMEOUT_MAX:
            raise ValueError(f'Must be > 0 and <= {self.TIMEOUT_MAX}')


    def _activate(self, procedure, *args, **kwd):
        # Operate TaskCreation API now.
        environ = kwd.pop('environ', dict())
        locals = kwd.pop('locals', None)
        progr = kwd.pop('programmer', None)
        user = kwd.pop('user', None)

        operator = kwd.pop('operator', None)
        audit = kwd.pop('audit', None)
        trace = kwd.pop('trace', None)
        account = kwd.pop('account', None)
        traceback = kwd.pop('traceback', None)
        init = kwd.pop('initialize', None)
        name = kwd.pop('name', None)
        timeout = kwd.pop('timeout', None)
        finishingScript = kwd.pop('finishing', '')

        environ.setdefault('trigger', self)
        environ.setdefault('environment', self.environment)
        environ.setdefault('doc', self.environment)
        environ.setdefault('path$', self._path)

        # todo: push remaining kwd into EmulatedCodeTaskCreation for executeGirl.

        create = dict(taskClass = Emulation, environ = environ,
                      operator = operator, audit = audit, trace = trace,
                      account = account, traceback = traceback,
                      initialize = init, name = name, timeout = timeout,
                      finishingScript = finishingScript,
                      programmer = progr, user = user,
                      procedure = procedure, locals = locals)

        task = EmulatedCodeTaskCreation.Create(self, **create)

        return self.Task(task, procedure)


    # def _activate(self, procedure, *args, **kwd):
    #     kwd['synchronous'] = bool(self.synchronous)

    #     try: environ = kwd.pop('environ')
    #     except KeyError: environ = dict()

    #     environ.setdefault('trigger', self)
    #     environ.setdefault('environment', self.environment)
    #     environ.setdefault('doc', self.environment)

    #     # User might differ from programmer setting as far as claimed identities.
    #     task = self._Emulation.Load(environ = environ, user = kwd.pop('user', None))

    #     try: task.operator = kwd.pop('operator')
    #     except KeyError:
    #         pass

    #     progr = kwd.pop('programmer', None)

    #     try:
    #         audit = kwd.pop('audit')
    #         if audit == 'debug':
    #             task.tracing = task.__class__.debugInstruction
    #         elif audit is True:
    #             task.tracing = task.__class__.auditInstruction

    #     except KeyError:
    #         try: task.tracing = kwd.pop('trace')
    #         except KeyError:
    #             pass

    #     # For billing API.
    #     try: account = kwd.pop('account')
    #     except KeyError: pass
    #     else:
    #         if account is not None:
    #             task.account = account

    #     procedure.setEnvironment(task.environ)

    #     try: locals = kwd.pop('locals')
    #     except KeyError:
    #         task.addFrameCall(procedure, arguments = args,
    #                           programmer = progr)
    #     else:
    #         task.addFrameCall(procedure, locals = locals,
    #                           arguments = args,
    #                           programmer = progr)

    #     finishingScript = kwd.pop('finishing', '')

    #     try: traceback = kwd.pop('traceback')
    #     except KeyError: pass
    #     else:
    #         try: runtime.call.System.Journal.waitLogs(task, traceback)
    #         except runtime.doesNotExist: pass

    #     try: init = kwd.pop('initialize')
    #     except KeyError: pass
    #     else: init(task) # A chance to construct memory-bound objects.

    #     try: name = kwd.pop('name')
    #     except KeyError: pass
    #     else: task.name = name

    #     try: timeout = kwd.pop('timeout')
    #     except KeyError: pass
    #     else:
    #         if timeout:
    #             self.checkValidTimeout(timeout)

    #             from world import heartbeat as vm
    #             from stuphos.kernel import Pure
    #             from ph.interpreter.mental.native import _setTimeout # todo: get from stuphos.kernel

    #             def terminateTask():
    #                 task.Terminate(task.machine)

    #             # environ['timeout$'] = \
    #             _setTimeout(vm, progr, Pure(terminateTask), timeout, None)


    #     # print(f'task.name: {task.name}')

    #     # Todo: don't return this (it's a decorator).  Until a replacement
    #     # can be written, be aware that this is returned to the girl code.
    #     onComplete = executeGirl(task, **kwd)

    #     if finishingScript:
    #         @onComplete
    #         def done(task, exception = None):
    #             # Spawn new task.
    #             newModuleTask(finishingScript, trigger = self,
    #                           completedTask = task)

    #     # @onComplete
    #     # def debugViewTermination(task, exception = None):
    #     #     debugOn()
    #     #     locals

    #     # Returned to the protected girl environment.
    #     return self.Task(task, procedure)

    def _activateAsync(self, procedure, task):
        # Used by asynchronous tasks to schedule evaluation.
        procedure.setEnvironment(task.environ)

        locals = dict(environment = self.environment,
                      doc = self.environment,
                      trigger = self)

        return task.frameCall(procedure, locals = locals)

    def _activateCheck(self, *args, **kwd):
        assert 'programmer' not in kwd, KeyError('programmer')
        assert 'operator' not in kwd, KeyError('operator')
        assert 'audit' not in kwd, KeyError('audit')
        assert 'trace' not in kwd, KeyError('trace')
        assert 'context' not in kwd, KeyError('context')

        return self._activate(*args, **kwd)

    def call(self, *args, **kwd):
        progr = vmCurrentTask().findProgrammer()
        return self._activate(self._module, *args,
                              **dict(environ = kwd,
                                     programmer = progr))

    def callForResult(self, *args, **kwd):
        return self.call(*args, **kwd).result()
    __call__ = callForResult


    @property
    def _evaluation(self):
        'Synchronous activation: wait for new task/frame call to execute.'

        from stuphos.kernel import Machine

        try: task = Machine.GetContextObject().task
        except AttributeError:
            # Not running within virtual machine task -- synchronously evaluate.
            # Note: there's no authority associated with this activation method.
            task = self._Emulation()

        return self._activateAsync(self._expression, task)

    class Task(writeprotected, Object):
        def __init__(self, task, procedure):
            self._task = task
            self._procedure = procedure

        @property
        def _onComplete(self):
            return self._task.onComplete

        @property
        def _result(self):
            return self._task.stack.pop()[0]

        # @property
        def result(self):
            # Marshalized Object and data.
            return outcomeOf(self._task, self._onComplete)


Evaluation = Trigger

class Inline(Trigger):
    @property
    def _module(self):
        return self.code

    @classmethod
    def _Build(self, ast, *args, **kwd):
        return self(Girl(Girl.Built, ast), *args, **kwd)

inline = Inline._Build

class View(writeprotected, Object):
    def register(self): # What is this used for?
        raise NotImplementedError
    def _render(self, request = None):
        raise NotImplementedError
    def _debugging(self, task, etype, value, tb):
        # Specifically, there was a bug during execution of the context trigger,
        # so this is a good place to generate a report page with task traceback.

        raise etype(value).with_traceback(tb) # there was a python bug


class NodePath(writeprotected, list):
    # __init__ = list.__init__

    def __init__(self, items):
        # Todo: whatever's constructing NodePath/DeepView must do this encoding..!
        # But this object maintains internal consistancy as a native object.
        # debugOn()
        list.__init__(self, (s.decode('utf-8') if isinstance(s, bytes)
                             else s for s in items))

    @property
    def _controlObject(self):
        return self

    def __getitem__(self, item):
        # Q: Why am I overriding this?
        result = list.__getitem__(self, item)
        if isinstance(item, slice):
            result = classOf(self._controlObject)(result)

        return result

    # def getElementAt(self, index):
    #     return list.__getitem__(self, index)
    def getTrailingElements(self):
        return vmNewSequence(list.__getitem__(self, slice(1, None, None)))

    @property
    def string(self):
        return '/'.join(self)

# @runtime.available(runtime.System.Journal)
# def debugging(log, self, etype, value, tb):

def debugging500(self, task, etype, value, tb):
    # import pdb; pdb.set_trace()

    # todo: generate html-ready (FO) tracebacks

    if isinstance(value, Processor.UncaughtError):
        etype = value.etype
        tb = value.tb

        if self.debug:
            vtb = '\n'.join(task._task.formatTraceback(value.traceback))

        value = value.value
    else:
        vtb = ''

    if not isYesValue(self.debug):
        # The idea at this point is that, because this is web view error
        # handling, but it is generally uncaught, we need to communicate
        # to the initiator (and the programmer) the things that we need
        # to.  If the site debug page is disabled, then the initiator
        # will basicaly get a 'didn't work' message.

        raise value.with_traceback(tb)

    # task.formatTraceback()

    # But we're mostly interested in python exception.
    if isYesValue(getConfig('native-traceback', 'Interpreter')):
        tb = '%s:\n%s\n' % (exceptionHeader(etype, value),
                            tracebackString(tb))
    else:
        tb = exceptionHeader(etype, value)

    from django.template.loader import get_template
    from django.template import Context
    from django.template.exceptions import TemplateDoesNotExist

    try: t = get_template('wm/500.html')
    except TemplateDoesNotExist:
        return tb

    return t.render(dict(traceback = tb, vtraceback = vtb,
                         task = task._task))

    # return 'Heres where we return a 500 template with traceback!'

class EmulatedView(View):
    __public_members__ = ['context', 'environment', 'source', 'debug', 'path', 'timeout']
    _debugging = debugging500

    class _Meta(Object._Meta):
        Attributes = ['_path']

    __repr__ = Object.__repr__

    DEFAULT_TIMEOUT = None

    def __init__(self, template, context, environment = None,
                 source = None, debug = False, path = '',
                 timeout = None):

        self._template = template
        self.context = context
        self.environment = environment
        self.source = source
        self.debug = debug
        self._path = path.split('/')
        self.timeout = timeout

    @property
    def path(self):
        return vmCurrentTask().sequence(self._path)

    def renderTemplate(self, **kwd):
        if self._template is None:
            return '' # kwd.get('content', '')

        return renderTemplate(self._template, **kwd)

    class _RequestAdapter(writeprotected, Object):
        def __init__(self, request):
            self.__request = request

        def __repr__(self):
            return f'<request$adapter {self.method} {self.path}>'

        @property
        def method(self):
            return getattr(self.__request, 'method', None)

        @property
        def path(self):
            return getattr(self.__request, 'path', None)

        @property
        def GET(self):
            try: return self.__GET
            except AttributeError:
                g = self.__GET = vmNewMapping(*list(self.__request.GET.items()))
                return g

        @property
        def POST(self):
            try: return self.__POST
            except AttributeError:
                g = self.__POST = vmNewMapping(*list(self.__request.POST.items()))
                return g

        # @property
        # def META(self):
        #     return vmNewMapping(*self.__request.META.items())
        @property
        def FILES(self):
            try: return self.__FILES
            except AttributeError:
                g = self.__FILES = vmNewMapping(*list(self.__request.FILES.items()))
                return g

        @property
        def userAgent(self):
            return self.__request.META['HTTP_USER_AGENT']


        class _User(writeprotected, Object):
            def __init__(self, user, request = None):
                self._user = user
                self._request = request

            def __repr__(self):
                if self._user is None:
                    return '<user$adapter$invalid>'

                return f'<user$adapter {self.username}>'

            @property
            def username(self):
                return self._user.username
            name = username

            @property
            def is_authenticated(self):
                return self._user.is_authenticated

            @property
            def is_superuser(self):
                return self._user.is_superuser

            @property
            def _primaryIdentity(self):
                return getPrimaryIdentity(self._user)

            @property
            def primaryIdentity(self):
                # User (Adapter) objects are passed to code running with other user permissions,
                # so we hide this.  For now, only current programmers can access their primary
                # identity.
                from stuphos.kernel import vmCurrentTask
                name = self._primaryIdentity
                lowerName = name.lower()

                progr = vmCurrentTask().findProgrammer()
                if progr is not None:
                    if progr.principal.lower() == lowerName:
                        return name

            @property
            def securityContext(self):
                # Note: requiring a login permission here complicates serving user-to-user
                # views, but we can't assume that the requesting user wants to give all
                # control to any other arbitrary user (besides the system) simply because
                # they're viewing the resource.  What is needed is user-specified ACL.
                from stuphos.kernel import securityContext, Programmer, vmCurrentTask
                principal = self._primaryIdentity
                vmCurrentTask().checkAccess(['system:user:context', principal], 'impersonate')
                return securityContext(Programmer(principal), user = self._user)


        @property
        def user(self):
            return self._User(self.__request.user, request = self.__request)

        @property
        def session(self):
            return # :security:
            return self.__request.session

        @property
        def body(self):
            return self.__request.body

        # provide access to persistant storage.

    def _render(self, request = None, response = None, account = None,
                path = None, requestAdapter = None, programmer = None,
                **ctxtdct):

        from stuphos.kernel import EmptyStackError
        from world import heartbeat as vm

        # *Call from an extra-heartbeat thread.
        q = Queue()

        progr = programmer
        # debugOn()
        # If progr.principal is '', then the interface doesn't have an owner.
        if programmer is None:
            # from phsite.network.models import DefaultPlayer
            from phsite.network.embedded.olc import WebProgrammer

            # Always use programmer specified (from interface setting),
            # but if it's None, get it from the primary identity.
            #
            # Since we're always using programmer, provide programmer-
            # setting security interface in native for the view.
            #
            if request is not None and request.user is not None \
                and request.user.is_authenticated:
                for d in request.user.default_players.all():
                    progr = WebProgrammer(d.player.player_name)
                    break

        def report(logger, task, traceback):
            # XXX is this being called?!
            logger.systemLog(task, traceback)

        ctxtdct['source'] = self.source
        # ctxtdct['view'] = self.path # Q: setdefault?
        contextObject = ctxtdct # todo: wrap to provide other services?

        if requestAdapter is None:
            if request is None:
                requestAdapter = None
            else:
                requestAdapter = self._RequestAdapter(request)

        locals = dict(request = requestAdapter)

        # locals['source'] = self.source

        protected = None # [None]
        environ = None

        def initializeTask(task):
            o = task.frame.locals

            # Convert source document into memory-safe structure.
            e = constrainStructureMemory(task, self.environment)
            o['environment'] = e
            o['doc'] = e

            # Store memory-safe mapping for response local.
            # p = protected[0] = task.memory.Mapping(task.memory, **response)
            # task.frame.locals['response'] = p

            nonlocal protected, environ
            with vm.threadContext(task = task):
                protected = task.memory.Mapping(task.memory, **response)
                o['response'] = protected

                task.environ = environ = task.shared_mapping(*contextObject.items())
                environ['context'] = environ
                environ['view'] = self.path

                o['path'] = task.sequence(path) if path is not None else None

        task = self.context._activate(self.context._module,
                                      name = f'view({path})',
                                      locals = locals,
                                      programmer = progr,
                                      traceback = report,
                                      account = account,
                                      initialize = initializeTask,
                                      timeout = self.timeout or self.getDefaultTimeout(),
                                      audit = 'debug' if self.debug =='debug' else None,
                                      user = request is not None and request.user or None)

        @task._onComplete
        def completeViewRequest(task, exception = None):
            # import game
            # game.syslog('view-request-context: %r' % ctxtdct)

            # print 'view-request-context: %r' % (exception,)

            if response is not None:
                # response.update(protected[0])
                response.update(protected)

            if exception:
                # Introspect into the ph runtime with debugging view.
                q.put((False, exception))
            else:
                # debugOn()

                try:
                    try: responseValue = task.stack.pop()
                    except EmptyStackError:
                        # Treat like returning None, for now.
                        responseValue = None

                    if isinstance(responseValue, str):
                        q.put((True, dict(content = responseValue)))
                    elif isinstance(responseValue, dict):
                        q.put((True, responseValue))
                    elif responseValue is not None:
                        raise TypeError(type(responseValue))
                    else:
                        # Re-acquire unicode/basestring type for renderTemplate call.
                        for (key, value) in environ.items():
                            if isinstance(key, bytes):
                                # del ctxtdct[key] # The bytes key.
                                ctxtdct[key.decode('ascii')] = value
                            else:
                                ctxtdct[key] = value

                        # todo: do as billable
                        q.put((True, self.renderTemplate(**ctxtdct)))

                except:
                    from sys import exc_info
                    q.put((False, exc_info()))

        (success, result) = q.get() # *
        if success:
            return result

        return self._debugging(task, *result) # response or raise


    class _DeepView(NodePath):
        def __init__(self, view, path):
            NodePath.__init__(self, path)
            self._view = view

        def __repr__(self):
            path = ', '.join(map(repr, self))
            return f'<deep-view on {self._view}: {path}>'

        @property
        def _controlObject(self):
            return self._view

        def _render(self, request = None, response = None, **ctxtdct):
            ctxtdct['path'] = self # todo: pass to render as keyword argument.
            return self._view._render(request = request, response = response,
                                      **ctxtdct)

    def lookup(self, *names):
        return self._DeepView(self, names)


    def getDefaultTimeout(self):
        return self.DEFAULT_TIMEOUT


RequestAdapter = EmulatedView._RequestAdapter
UserAdapter = RequestAdapter._User


# from stuphos.kernel import LibraryView as libView
# from django.views.decorators.csrf import csrf_exempt

# class LibraryView(libView):
#     'CMS Library View bound to node configuration.'

#     @runtime.available(runtime.Agent.System)
#     @csrf_exempt
#     def render(core, self, request = None, response = None, **ctxtdct):
#         return libView.render(self(request, core), self.path)

#     def __init__(self, path):
#         self.path = path


import codecs
from hashlib import sha256

class StaticView(View):
    __public_members__ = ['content', 'content_type']

    def __init__(self, content, content_type = None):
        self.content = content
        self.content_type = content_type

    def _render(self, *args, **kwd): # request = None, response = None, account = None):
        return self.content

    @property
    def nonce(self):
        return codecs.encode(sha256(self.content).digest(), 'base64')

class AliasedView(View):
    __public_members__ = ['path']

    def __init__(self, path):
        if isinstance(path, str):
            path = path.split('/')

        if not isinstance(path, (list, tuple)):
            raise TypeError(type(path).__name__)

        self.path = path

    class _recursionGraph(set):
        def __init__(self, initial):
            self.add('/'.join(initial))

        def __call__(self, new):
            new = '/'.join(new)
            if new in self:
                # Recursion detected.
                return True

            self.add(new)

    def _render(self, request = None, **kwd):
        from ph.interpreter.mental.library.views import renderWM

        # Recursion control.
        graph = kwd.pop('aliasGraph', None)
        if graph is None:
            graph = self._recursionGraph(self.path)
        else:
            if graph(self.path):
                raise RecursionError('Alias recursion detected!')

        kwd.pop('path', None) # Already passed as positional argument.
        kwd.pop('programmer', None) # Passed later as positional arg.
        kwd.pop('account', None) # Not permitted by renderView.

        ctx = dict(aliasGraph = graph)

        return renderWM(request, request.user, self.path, ctx, **kwd)


class HtmlView(View):
    '''
    (stuph$html):
      html:
        - head:
          - title: 'The webpage title'
          - style:
              type: 'text/css'
              .content::
                body { margin: 10px }

        - body:
          - div: 'This is the content'
          - button:
              .content: 'Ok?'
              onclick::
                alert('Ok');
    '''

    __public_members__ = ['document']

    def __init__(self, root, context):
        self.document = root
        self._context = context

    _blacklist_element = []
    _blacklist_attribute = {}
    _blacklist_attribute_star = []

    def _render(self, request = None, response = None):
        def buildMap(xxx_todo_changeme):
            (name, items) = xxx_todo_changeme
            if name in self._blacklist_element:
                return ''

            bla = self._blacklist_attribute.get(name, [])
            attrs = []

            if isinstance(items, dict):
                content = ''
                children = []

                for (k, v) in items.items():
                    if k == '.content':
                        content = v
                    elif k == '.children':
                        children = v
                    else:
                        if not k in bla and k not in self._blacklist_attribute_star:
                            # todo: render v structural item
                            v = repr(v).replace('\\n', '\n').replace('\\t', '\t')
                            attrs.append('%s=%s' % (k, v))

                def buildChildren():
                    for c in children:
                        yield build(c)
                    if content:
                        # todo: escape html entities in content
                        # or, render structural item
                        # or, transform other markup
                        yield content

                children = nls(buildChildren())

            elif isinstance(items, list):
                children = nls(mapi(build, items))
            else:
                children = str(items)

            attrs = ' '.join(attrs)

            return '<%s%s%s>\n%s\n</%s>\n' % (name, attrs and ' ' or '',
                                              attrs, indent(children), name)

        def build(node):
            if isinstance(node, dict):
                return ''.join(mapi(buildMap, iter(node.items())))

            elif isinstance(node, list):
                return nls(mapi(build, node))

            else:
                try: r = node.render
                except AttributeError: pass
                else:
                    return str(r())

            return ''

        return build(self.document)

    class _ScriptElement(writeprotected):
        __public_members__ = ['item']

        def __init__(self, item):
            self.item = item

        def render(self):
            return ''

class Template(writeprotected, Object):
    def __init__(self, template):
        self._template = template

    def renderTemplate(self, *args, **kwd):
        for a in args:
            if isinstance(a, (list, tuple)):
                a = dict(a)
            if isinstance(a, dict):
                kwd.update(a)

        return renderTemplate(self._template, **kwd)

    render = __call__ = renderTemplate
    rendering = property(renderTemplate)


class Streaming(writeprotected, Object):
    __public_members__ = ['handler']

    def __init__(self, handler):
        self.handler = handler

    def __call__(self, request, *args, **kwd):
        # todo: setup new task environ with request, and execute handler.
        pass

class EqSet(writeprotected, AutoMemoryMapping):
    def equip(self, ch):
        # :security: native exposure.
        machine.checkAccess(['game:equip'])

        import world
        for (where, vnum) in self.items():
            i = world.item(vnum).instantiate(ch)
            try: ch.equip(i, where)
            except IndexError:
                pass # i.extract()

    __call__ = equip

class AuctionList(writeprotected, AutoMemorySequence):
    def __init__(self, sequence):
        AutoMemorySequence.__init__(self, sequence)
        # self.registerAll()

    def registerAll(self):
        for item in self:
            item.register()
        return self
    __call__ = registerAll


# URLConf patterns.
class UrlConfiguration(writeprotected):
    def __init__(self, value):
        self._patterns = []

        if not isinstance(value, (list, tuple)):
            raise TypeError(type(value).__name__)

        for conf in value:
            if not isinstance(conf, dict):
                raise TypeError(type(conf).__name__)
            if len(conf) != 1:
                raise ValueError(f'{len(conf)}') # : {conf.keys()}')

            (pattern, handler) = next(iter(conf.items()))
            self._patterns.append(UrlPattern(pattern, handler))

    def lookup(self, url, include_pattern = False):
        for pattern in self._patterns:
            match = pattern(url)
            if match is not None:
                if include_pattern:
                    return vmCurrentTask().sequence((pattern, match))

                return match

    __getitem__ = lookup


    @nling
    def __str__(self):
        for (i, pattern) in enumerate(self):
            yield f'#{i}. {pattern._pattern.pattern} -> {pattern.handler}'


import re
class UrlPattern(writeprotected):
    __public_members__ = ['handler']

    def __init__(self, pattern, handler):
        if isinstance(handler, dict):
            handler = handler['handler']

        if isinstance(handler, str):
            handler = handler.split('/')

        if not isinstance(handler, (list, tuple)):
            raise TypeError(type(handler).__name__)

        self._pattern = re.compile(pattern)
        self.handler = handler

    def __repr__(self):
        return f'<pattern {repr(self._pattern.pattern)}: {self.handler}>'

    def __call__(self, input):
        match = self._pattern.match(input)
        if match is not None:
            return UrlMatch(match, self.handler)


from stuphos.kernel import StringValue

class UrlMatch(writeprotected):
    def __init__(self, match, handler):
        self._match = match
        self._handler = handler
    def __call__(self):
        return vmCurrentTask().sequence(self._match.groups())

    @property
    def handler(self):
        return vmCurrentTask().sequence(self._handler)

    @property
    def handlerString(self):
        return StringValue('/'.join(self._handler))


class containerAccessor(writeprotected):
    # Protected structural accessor object.

    def __init__(self, object):
        self._object = object

    def __getitem__(self, item):
        value = self._object[item]
        if isinstance(value, (dict, list, tuple)):
            return containerAccessor(value)

        return value


class Factory(Submapping):
    from .db.vardb import db, table

    def trigger(self, name, value, **kwd):
        from stuphos.language.document.interface import getContextEnvironment

        if isinstance(value, str):
            code = value
            synchronous = False
        else:
            code = value['code']
            synchronous = value.get('synchronous', False)
            if synchronous:
                raise RuntimeError('Synchronous triggers not allowed!') # Keep this for now. :security:

        # Todo: kwd['container'] is a dict (not a Building.Item)
        env = containerAccessor(kwd['container'])

        # For relative dotlevel path lookups.
        path = getContextEnvironment('document', default = None)
        return Trigger(code, synchronous, env, path = path)

    task = let = evaluation = code = trigger

    def emulation(self, name, value, **kwd):
        return None

        # Todo: Pass a procedure/module and emulate a buffered version of those instructions.
        if isinstance(value, grammar.Node):
            pass # validated, but compile todo
        elif not isinstance(value, str):
            raise TypeError(type(value))

        # todo: compile the value?
        # value = Girl(Girl.Module, value)

        from stuphos.system.api import game
        task = game.emulateTask(value) # as module?
        return Trigger.Task(task, None)

    def view(self, name, value, **kwd):
        content_type = None

        if isinstance(value, str):
            content = value
        else:
            try: content = value['content']
            except TypeError as e:
                content = str(e)

            except KeyError:
                # Build an emulator program for rendering data.
                template = value.get('template', None)
                context = value['context']
                timeout = value.get('timeout', None)

                env = containerAccessor(kwd['container'])

                return EmulatedView(template, context, env,
                                    # todo: 'onerror: traceback'
                                    debug = value.get('debug', False),

                                    # XXX I thought this was: stuphos.language.document.interface.getContextEnvironment('document')
                                    source = kwd.get('document'), # source is a positional keyword in mud.lang.structure.document

                                    path = name, # XXX use document loader path, since this is relative
                                    timeout = timeout)

            else:
                content_type = value.get('content-type')

        return StaticView(content, content_type = content_type)

    def alias(self, name, value, **kwd):
        return AliasedView(value)


    def include(self, name, value, **kwd):
        raise NotImplementedError('Experimental')

        if isinstance(value, str):
            value = value.split('/')

        if not isinstance(value, (list, tuple)):
            raise TypeError(type(value).__name__)

        task = vmCurrentTask()
        return task.native.structure(task.frame, value)


    def urlconf(self, name, value, **kwd):
        return UrlConfiguration(value)
    patterns = urlconf


    # def libraryView(self, name, value, **kwd):
    #     return LibraryView(value)

    def template(self, name, value, **kwd):
        return Template(value)

    def streaming(self, name, value, **kwd):
        return # Streaming(self.trigger(name, value, **kwd))

    def html(self, name, value, **kwd):
        return # HtmlView(value, kwd)

    def encoded(self, name, value, **kwd):
        return # value.decode('base64')
    def zencoded(self, name, value, **kwd):
        return # value.decode('base64').decode('zlib')

    def configuration(self, name, value, **kwd):
        return # XXX Provide native-supported Configuration impl.

        from io import StringIO
        from configparser import ConfigParser
        from .management.config import Configuration

        cfg = ConfigParser()
        cfg.readfp(StringIO(value))

        return Configuration(cfg, name)

    # def pgAuth(self, name, value, **kwd):
    #     from .management.db import dbCore
    #     value['type'] = 'pg-auth'
    #     return dbCore.installConfiguration(name, **value)

    def planet(self, name, value, **kwd):
        return # XXX use spatial api

        from stuphmud.server.zones import Planet # , core
        p = Planet(value['vnum'], value['name'], value['object'])
        for c in value.get('continents', []):
            p.newContinent(c['vnum'], c['name'], c['object'])

        # p._enterSystem(mud.zones.core)
        return p

    def eqSet(self, name, value, **kwd):
        return # XXX Use native-supported constraint for item.

        if isinstance(value, dict):
            return EqSet(value)

    def auctionItem(self, name, value, **kwd):
        return # XXX Use native-supported constraint for item.

        item = runtime[runtime.StuphMUD.Auction].Item \
               (-1, value['vnum'], name, value['minlevel'], value['minbid'], 0,
                description = value.get('description', ''),
                payload = value.get('payload', ''))
        return item

    def auction(self, name, value, **kwd):
        return # AuctionList(iter(value.values()))

    # Returns a non-native-safe object.
    # from stuphmud.server.magic.structure import spell
    # spell = staticmethod(spell)

    def rst(self, name, value, **kwd):
        from docutils.core import publish_parts
        return MemoryMapping(publish_parts(value, writer_name = 'html'))

    def quest(self, name, value, **kwd):
        # :security: internal load
        # return # todo: move into tool

        from ph.emulation.machine import vmCurrentTask
        try: task = vmCurrentTask()
        except AttributeError: return
        task.checkAccess(['zones:autoquest'], 'create')

        from stuphmud.server.zones.specials.autoquest import loadQuest

        VALID_QUEST_TYPES = ['$builtin.ProtectedSenario']

        assert value['quest-type'] in VALID_QUEST_TYPES
        return loadQuest(value, source = kwd.get('document', []) + [name])

    def value(self, name, value, **kwd):
        return value # identity

    # def synthetic(self, name, value, **kwd):
    #     return Synthetic(value)

    def url(self, name, value, **kwd):
        # :security: XXX unsafe load package
        raise NotImplementedError('Blocking unsafe operation')

        from phsite.network import url, importView, patterns, include_urlpatterns
        try:
            try: value = value['include']
            except KeyError:
                view = value['view'].split('.')
                viewModule = '.'.join(view[:-1])
                viewName = view[-1]

                view = importView(viewModule, viewName)
                try: view = view.view
                except AttributeError:
                    pass

                return url(value['pattern'], view)
            else:
                if isinstance(value, list):
                    return patterns('', value)

                from stuphmud.server.runtime import LookupObject
                include = LookupObject(value['package']).urlpatterns
                return include_urlpatterns(value['pattern'],
                                           include)

        except Exception as e:
            return e

        '''
        patterns:
          - (stuph$url):
            pattern: '^/html/format$'
            view: person.services.web.views.format_html
          - (stuph$url):
            include:
              pattern: '^game/'
              package: web.stuph.embedded.urls
          - (stuph$url):
            include:
            - (stuph$url):
              pattern: '^accounts/profile'
              view: web.stuph.accounts.profile
        '''

    def library(self, name, value, **kwd):
        # XXX This introduces a lowlevel object that has no memory management.
        raise NotImplementedError('Blocking unsafe operation')

        return LibraryCore(value.getSection('LibraryCore'),
                           LibraryCore.Node)

    class factory(Object, object):
        '''
        my/application:
            interfaces/interface::
                object($submapping):
                    classes:
                        object: my/components/object/kernel

                    document::
                        component($object): true


            documents/usage::
                structure('my/application/interface').object.component

                '''

        def __new__(self, name, value, **kwd):
            raise NotImplementedError

            core = runtime[runtime.Agent.System]
            if not core:
                raise NotImplementedError('%s not installed' % runtime.Agent.System)

            try: classes = value['classes']
            except NameError:
                classes = value
                document = None
            else:
                document = value['document']

            # Todo: merge parent-document 'value' structure into sub-document result object?

            f = object.__new__(self, core, name, classes, **kwd)
            f.__init__(core, name, classes, **kwd)

            if document is None:
                return f

            # Load sub-document.
            return f(document, **kwd) # kwd env?


        def __init__(self, core, name, classes, **kwd):
            self._classes = dict((n, self._lookupSubmapping(core, v))
                                 for (n, v) in classes.items())

        def _lookupSubmapping(self, core, n):
            s = n.split('/')

            for i in range(len(s), -1, -1):
                n = s[:i]

                try: n = core.lookup(*n) # XXX won't the Node.Tool just dereference its scope..?
                except KeyError:
                    continue

                if isinstance(n, core.Node.Tool):
                    n = n.scope

                    for o in s[i:]:
                        n = getattr(n, o) # todo: catch AttributeError and restart library search?


                    # An object was found, now decide what to do with it.

                    # if isinstance(n, Submapping):
                    #   return n


                    # SECURITY NOTE:  Because structures are intended to be loaded from the
                    # virtual machine, they are restricted to only loaded native tool library
                    # paths, which should only be producing object encapsulations.
                    #
                    # Additionally, native tool structural objects must be loaded from the
                    # tool's "_Factory" object, because structural item building methods do
                    # not take frame parameters.  Instead, the factory must detect the vm's
                    # task context instance if it needs to do frame-dependent actions.

                    return n._Factory


                if isinstance(n, core.Node.Module):
                    return self._activity(self, core, n, s)


        @property
        def _machine(self):
            from world import heartbeat as vm
            return vm
            return runtime[runtime.System.Engine]

        def __call__(self, source, **env):
            from stuphos.language.document.interface import load

            def coprocess():
                # XXX object-load/instantiation order is arbitrary!
                return load(source, self._classes, '', **env)

            try: task = self._machine.taskObject # contextObject.task
            except AttributeError:
                return coprocess()
            else:
                # a parallel document-loading routine object that submaps to library activities
                # and when loading, evaluates the instantiations asynchronously

                # XXX it's not asynchronous, it's callAsynchronous, or some bullshit.
                task.callAsynchronous(coprocess)


        class _activity:
            def __init__(self, submapping, core, node, segments):
                self._submapping = submapping
                self._core = core
                self._node = node
                self._segments = segments

            def __call__(self, name, value, **kwd):
                from stuphos.kernel import LibraryNode, Script, findCurrentUser
                from world import heartbeat as vm

                with vm.Loading(Script, environ = kwd, user = findCurrentUser()) as task:
                    lib = LibraryNode._WithCore(self._core, self._node, self._segments)
                    instance = lib.instantiate(arguments = dict(value = value))

                    @task.onComplete
                    def buildComplete():
                        # Hack the stack to assert an exact task return value.
                        task.stack[:] = [instance]


                    # Wait for the virtual task to complete, and return the
                    # object result inserted from the activity instantation.
                    # Todo: errors.
                    return task.returnValue


    submapping = factory

    def structure(self, name, value, **kwd):
        '''
        my/application:
            interfaces/interface::
                object($structure):
                    classes:
                        # The path is to a Native Tool with a Factory definition.
                        '': my/components/object/kernel

                    document::
                        # object is defined in the native tool factory.
                        component($object): true


            documents/usage::
                structure('my/application/interface').object.component


        '''

        # This can wrap a factory.
        raise NotImplementedError('Blocking unsafe operation')

        core = runtime[runtime.Agent.System]
        if core is not None:
            classes = value['classes']
            document = value['document']
            default = value.get('default', '') # 'stuph'

            if isinstance(classes, self.factory):
                classes = classes._classes
            else:
                def factory(path):
                    node = core[path]
                    if isinstance(node, core.Node.Module):
                        # Todo: invoke method (like call) within activity.
                        # Because this means raising a Continuation that a
                        # would require a rewrite of the document loading
                        # code, we can do it synchronously, waiting on
                        # invocations in the outer-frame but this must be
                        # done from a non-heartbeat thread!  So, move the
                        # document load into a pooled thread executor.
                        pass
                    elif isinstance(node, core.Node.Structure):
                        pass

                    elif isinstance(node, core.Node.Tool):
                        # XXX check permission.
                        return node.scope._Factory

                classes = dict((type, factory(path))
                                for (type, path) in classes)

            # from mud.lang.structure import Factory
            # classes['stuph'] = Factory

            from stuphos.language.document.interface import load
            return load(document, classes, default)


    class _MethodInterface(Subroutine.Interface):
        # As a Subroutine.Interface, this object is callable by the emulation
        # runtime by dereferencing the procedure.  This object generates new
        # subroutine instances on property dereference for individual frames.

        def __init__(self, module, name, **env):
            self._module = module
            self._name = name
            self._environ = env

        @property
        def _programmer(self):
            # Used by call instruction.
            return self._environ.get('programmer')

        @property
        def _subroutine(self):
            return self._module.getSubroutine(self._name)
        _procedure = _subroutine

        # @property
        # def _activation(self):
        #     proc = self._procedure # Dereference a Subroutine.
        #     return Invocation(proc.main_program, proc.name, proc.start_position)

        def __repr__(self):
            return f'<method$interface {repr(self._name)}>'


    def method(self, name, value, **kwd):
        # Not really sure what the point of this is, to be part of
        # a synthetic (structural) class.  It could be wrapped by
        # something to mark it and get passed to the class constructor,
        # but, a method definition really has no use alone.
        module = buildMethodFromStructure(name, value, **kwd)

        from stuphos.kernel import Girl
        module = Girl(Girl.Module, module)

        # module.setEnvironment(vmCurrentTask().environ)

        # Get the owner of the (agent system) interface, if it exists.
        # from stuphos.language.document.structural import Context
        # progr = Context['loader'].environ.get('programmer')

        from stuphos.language.document.interface import getContextEnvironment
        progr = getContextEnvironment('programmer', default = None)

        return self._MethodInterface(module, name, programmer = progr)

    procedure = subroutine = method


    # Currently fails.  Also, returns a non-native-safe object.
    # from stuphos.language.shortate import shortate
    # shortate = staticmethod(shortate)


    def command(self, name, value, **kwd):
        # XXX Provide a memory-sensitive implementation of actionable.command[.verb]
        raise NotImplementedError('Blocking unsafe operation')

        # Requires implementation.
        from spatial.architecture import actionable

        if isinstance(value, str):
            value = dict(implementation = value)

        parse = value.get('parse')

        if isinstance(parse, str):
            parse = buildMethodFromStructure(parse, **kwd)

        impl = value['implementation']

        if isinstance(impl, str):
            impl = buildMethodFromStructure(impl, **kwd)

        # if isinstance(parse, subroutine):
        #   parse = compileSubroutine(parse)
        # if isinstance(impl, subroutine):
        #   impl = compileSubroutine(impl)


        ns = dict(__call__ = impl)
        if parse is not None:
            ns['parseArgs'] = parse


        verbClass = newClassType('implementation', (actionable.command.verb,), ns)
        ns = dict(name = name, implementation = verbClass)

        return newClassType('%sCommand' % name, (actionable.command,), ns)


identifier_pattern = re.compile('[a-zA-Z$_][a-zA-Z$_0-9]*').match
def isValidIdentifier(name):
    return identifier_pattern(name) is not None

def buildMethodFromStructure(name, value, **kwd):
    if not isValidIdentifier(name):
        # If it's coming from structure, validate.
        raise NameError(name)

    if isinstance(value, str):
        parameters = []
        code = value
    else:
        parameters = value['parameters']
        code = value['code']

    parameters = ', '.join(parameters)
    return buildMethod(name, parameters, code)

def buildMethod(name, parameters, code = 'pass'):
    # from ph.lang.layer import grammar
    # ast = grammar.Grammar.AST

    # suite = ast.Suite([])
    # module = ast.Suite([ast.FunctionDefinition(name, parameters, suite)])

    code = 'locals().update(keywords$())\n' + code

    return 'def %s(%s):\n%s\n' % (name, parameters, indent(code))


@staticmethod
def htmlScript(name, value, **kwd):
    # XXX value must be interned here, meaning a memory mapping or sequence,
    # otherwise, structural.Items won't be constrained by mental.objects code.
    raise NotImplementedError('Blocking unsafe operation')

    return HtmlView._ScriptElement(value)

#@staticmethod
def syntheticClass(name, value, **kwd):
    from stuphos.kernel import Girl, SyntheticClass

    # todo: $classInit$ trigger method for initializing
    # environment.  Also, pass kwd/document container
    # for connecting class impl to structure.

    attributes = []
    def checkMember(n, m):
        if isinstance(m, (dict, str)):
            return True

        attributes.append((n, m))
        return False

    methods = ((n, m) for (n, m) in value.items()
               if checkMember(n, m))

    synth = SyntheticClass \
            (name,
             Girl(Girl.Module,
                  nls(buildMethodFromStructure(defn, m, **kwd) for
                      (defn, m) in methods)),
             kwd.get('container'))

    for (n, m) in attributes:
        # todo: is this right?  Shouldn't it be set in environ?
        setattr(synth, n, m)

    # Note: classInit must be called by client.
    return synth


setattr(Factory, 'html.script', htmlScript)
setattr(Factory, 'class', syntheticClass)
Factory.object = Factory.formula = getattr(Factory, 'class')

from stuphos.kernel import GirlCore
class LibraryCore(GirlCore):
    def loadEntities(self, cfg, nodeClass):
        pass
    def saveNode(self, node, recurse = False):
        pass
    def destroyNode(self, node):
        pass


class SystemFactory(Submapping):
    def tool(self, path, sourceCode, **kwd):
        segments = path.split('/')
        assert isinstance(sourceCode, str)
        core = runtime[runtime.Agent.System]
        assert core is not None
        scope = Core.Python().module(path, sourceCode,
                                     container = kwd['container'])
        return core.addPythonTool(segments, scope) # Q: dictOf()?

    # def lock(self, name, value, **kwd):
    #   from threading import Lock
    #   return Lock()
