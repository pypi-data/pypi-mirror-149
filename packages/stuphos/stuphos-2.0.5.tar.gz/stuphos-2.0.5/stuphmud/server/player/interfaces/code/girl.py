# Connects Girl interpreter to player shell/command experience.
# import new

from stuphos.kernel import Girl, Script, Volume, Undefined, Programmer
from stuphos.kernel import GirlSystemModule, Machine as VM, GrammaticalError
from stuphos.kernel import findUserByName, OuterFrame, TaskCreation
from stuphos.runtime import Object
from stuphos import getConfig
from stuphmud.server.player import getPlayerScope, events, HandleCommandError
from stuphmud.server.player.interfaces.code import ShellFactoryBase
from stuphmud.server.adapters import PeerAdapter, MobileAdapter, TriggerAdapter
from stuphos.etc.tools import getKeyword, Option, isYesValue
from . import ProgrammeManager, EvaluationShell, Programme, isFromSecureHost

# Permission level for non-authenticated command users.
DEFAULT_PROGRAMMER = Programmer.NONE

COMMAND_TASK = "call('player/interpreter/command', me, command, subcommand, arguments)"
# COMMAND_TASK = "'player/interpreter/command'(me, command, subcommand, arguments)"

VERB_TASK = "return call('player/interpreter/verb', me, command, arguments)"
# VERB_TASK = "return 'player/interpreter/verb'(me, command, arguments)"

class EvaluateCodeTaskCreation(TaskCreation):
    def __init__(self, peer = None, completion = None, initialize = None,
                 *args, **kwd):
        TaskCreation.__init__(self, *args, **kwd)

        self.peer = peer
        self.completion = completion
        self.initialize = initialize
        # self.environ = environ

        if peer is None:
            self.programmer = DEFAULT_PROGRAMMER
            self.user = None
        else:
            name = peer.avatar.name
            self.programmer = Programmer(name)
            self.user = findUserByName(name)

        self.taskClassKwd = dict(user = self.user)

    def createTask(self, environ):
        task = TaskCreation.createTask(self, environ)
        task.environ.update(**self.environScope)

        # print(f'[evalCode.createTask] {dict.keys(task.environ)}')

        self.procedure.setEnvironment(task.environ)

        return task

    def postInitTask(self, task, frame):
        user = self.user
        if user is not None:
            self.locals._connectMemory(VM.Task.Memory.Connect(task, user))

        if self.completion:
            frame.onComplete(self.completion)

        if self.initialize:
            self.initialize(task)

        return TaskCreation.postInitTask(self, task, frame)


# Implementation of VM.Task.
class PlayerScript(Script):
    def __init__(self, peer, shell, tracing, *args, **kwd):
        self.peer = peer
        self.shell = shell

        Script.__init__(self, *args, **kwd)

        self.uncaughtError = self.handleError

        if tracing:
            # debugOn()
            self.tracing = self.traceToConsole

            if tracing == 'stack':
                self.debugStack = True


    def frameOneForPeer(self, peer, *args, **kwd):
        return Script.frameOne(self, *args, **kwd)

    def frameOne0(self, *args, **kwd):
        # if 0:
        #     # :console: :debugging:
        #     import sys
        #     print >> sys.stderr, 'Frames:', len(self.frames)
        #     # print >> sys.stderr, '\n'.join(str(f.procedure) for f in self.frames)
        #     p = self.frame.procedure
        #     if hasattr(p, 'position'):
        #         o = p.position(0)
        #         print >> sys.stderr, p.instructionsString(o, o+1)

        # Swap in peer for console.
        # try: return self.shell.withPeerHeadAndException(self.peer, (self.Done, VM.Yield),
        #                                                 self.frameOneForPeer,
        #                                                 *args, **kwd)
        # # except Script.Yield:
        # #     import sys
        # #     (etype, value, tb) = sys.exc_info()
        # #     raise (etype, value, tb)

        # except Script.Done, e:
        #     # This is not necessary in all cases of Script.Done at this level.
        #     # This is because Done is also raised on exception, in which case
        #     # the stack is not REPL-integrated.
        #     # try: result = self.stack.pop()[0]
        #     # except IndexError: pass
        #     # else:
        #     #     if result is not None:
        #     #         print >> self.peer, repr(result)

        #     raise e

        return self.shell.withPeerHeadAndException \
                    (self.peer, (self.Done, VM.Yield),
                     self.frameOneForPeer,
                     *args, **kwd)

    def handleError(self, task, frame, exc, traceback):
        # XXX Emitting no error for some things but still raising Done.
        (etype, value, tb) = exc
        if isinstance(value, VM.Yield):
            return # This may not be right since it might need to be propogated.
            raise etype(value).with_traceback(tb)

        if isYesValue(getConfig('native-traceback', 'Interpreter')):
            HandleCommandError(self.peer, exc, frame_skip = 0)

        self.peer.sendTraceback(self, exc, traceback)

        # Eventually this will go away in favor of traceback logging.
        if isYesValue(getConfig('report-player-error', 'Interpreter')):
            from traceback import print_exception as pe
            print('player error:')
            pe(*exc)

        self.logTraceback(task, traceback)
        raise self.Done


    traceToConsole = Script.debugInstruction

    # def traceToConsole(self, frame, pos, instr, args):
    #     # debugOn()
    #     task = frame.task

    #     try: name = frame.procedure.getSourceMap().source
    #     except AttributeError:
    #         name = task.name

    #     instr = getattr(instr, '__name__', '?')
    #     args = ', '.join(map(str, args))

    #     msg = '%-20.20s %04d %s(%s)' % (name, pos, instr, args)

    #     print(msg)
    #     if task.stack:
    #         # Don't print anything if there's no stack, otherwise
    #         # it will look like an empty string on the stack.
    #         print('    ' + '\n    '.join(map(str, task.stack)))

    def handleVerbOutcome(self, outcome, command, argstr):
        # Override this in a new script class for custom command recognition.
        if not outcome:
            print('Unknown command: %r' % command, file=self.peer)


    # Invocation Methods:
    @classmethod
    def evaluateCodeAsync(self, peer, shell, program, scope, completion,
                          tracing = False, check_active = True,
                          initialize = None,
                          **environ):

        # Because this code starts and runs code with a certain authorization, we make
        # a determination in our security model if that authority passes the check.
        if isFromSecureHost(peer):
            kwd = dict(peer = peer, vm = getVirtualMachine(), procedure = program,
                       taskClass = self, taskClassArgs = (peer, shell, tracing),
                       locals = scope, completion = completion, environ = environ,
                       checkActiveTasks = check_active)

            return EvaluateCodeTaskCreation.Create(**kwd)


    # @classmethod
    # def evaluateCodeAsync(self, peer, shell, program, scope, completion,
    #                       tracing = False, check_active = True, **environ):

    #     # Because this code starts and runs code with a certain authorization, we make
    #     # a determination in our security model if that authority passes the check.
    #     if isFromSecureHost(peer):
    #         # from stuphos.etc import isYesValue
    #         # from stuphos import getConfig

    #         if peer.avatar is None:
    #             progr = DEFAULT_PROGRAMMER
    #             user = None
    #         else:
    #             name = peer.avatar.name
    #             progr = Programmer(name)
    #             user = findUserByName(name)


    #         # Start new PlayerScript task.
    #         if check_active:
    #             # This might have been done before compiling the program.
    #             from stuphos.kernel import checkActiveTasks
    #             checkActiveTasks(user)

    #         task = self(peer, shell, tracing, user = user)
    #         task.environ.update(**environ)

    #         # This is for a persistance concept that doesn't yet exist so it should be removed.
    #         # task.environ['book'] = Volume(getattr(peer, 'environ', task.environ), program) # or scope

    #         # if isYesValue(getConfig('system-module', 'AgentSystem')):
    #         #     task.environ['system'] = GirlSystemModule.Get()

    #         program.setEnvironment(task.environ)


    #         vm = getVirtualMachine()
    #         new = task.addFrameCall(program, programmer = progr)
    #         new.locals = scope
    #         if user is not None:
    #             # Note: scope must be a managed memory object.
    #             # Todo: make it vm.Task...?
    #             scope._connectMemory(VM.Task.Memory.Connect(task, user))

    #         if completion:
    #             # print(f'registering completion: {completion}')
    #             new.onComplete(completion)

    #         vm += task
    #         return task

    class reprCompletion:
        def __init__(self, peer):
            self.peer = peer

        def __call__(self, frame, *error):
            task = frame.task
            if task.stack and error[1] is None:
                try: value = task.stack.pop()[0]
                except IndexError: pass
                else: self.displayValue(value)

        def displayValueToPeer(self, reprValue):
            if isinstance(reprValue, str):
                # todo: move actual printing to method on peer.
                # print(f'task return value: {value}')
                print(reprValue, file = self.peer)

        def displayValue(self, value):
            if value is not None:
                # debugOn()

                try: _reprc = value._reprOrContinuation
                except AttributeError as e:
                    # print(f'display value _reprc: {e}')
                    value = repr(value)
                else:
                    # If this returns None, there was a continuation.
                    value = self.runDisplayValue(_reprc, value)

                self.displayValueToPeer(value)

        def runDisplayValue(self, _reprc, value):
            # return repr(value)

            # Run the repr method in this task!

            try: return _reprc()
            except OuterFrame as sub:
                @sub.onComplete
                def reprCompleted(frame, *error):
                    if error[1] is None:
                        self.displayValueToPeer(frame.task.stack.pop()[0])

            # except Exception as e:
            #     print(f'[display] {e.__class__.__name__}: {e}')
            #     raise e


        # elif isinstance(error[1], task.frames.ForeignFrameError):
        #     frame = error[1].frame
        #     print >> peer, 'foreign:', frame #.procedure

    @classmethod
    def evaluateCode(self, peer, shell, program, scope, tracing = False, **environ):
        return self.evaluateCodeAsync(peer, shell, program, scope,
                                      self.reprCompletion(peer),
                                      tracing = tracing, **environ)

    @classmethod
    def evaluateInput(self, peer, type, input, tracing = False, shell = None):
        return self.evaluateInputAsync(peer, type, input, self.reprCompletion(peer),
                                       tracing = tracing, shell = shell)

    @classmethod
    def evaluateInputAsync(self, peer, type, input, completion, tracing = False, shell = None):
        scope = getGirlPlayerScope(peer) # target of @dir()
        program = Girl(getattr(Girl, type.capitalize()), input)

        if shell is None:
            shell = peer.interpreter

        if isYesValue(configuration.Interpreter.dump_expression_code):
            peer.sendln(program.instructionsString())

        self.evaluateCodeAsync(peer, shell, program, scope, completion,
                               tracing = tracing,
                               this = PeerAdapter(peer), # todo: persist these
                               me = MobileAdapter(peer.avatar))

        return True

    @classmethod
    def evaluateStatement(self, peer, statement, tracing = False, shell = None):
        return self.evaluateInput(peer, 'statement', statement, tracing = tracing, shell = shell)

    @classmethod
    def evaluateScript(self, peer, script, tracing = False, shell = None):
        return self.evaluateInput(peer, 'module', script, tracing = tracing, shell = shell)


    # Command/Verb invocation: the interpreter is a running task that is stored
    # as a weakref on the peer object, started by this class if it is not already
    # running (evaluates as non-None).  Commands and verbs are merely objects
    # passed to this running task using a synchronization queue.  The interpreter
    # program is responsible for sequencing the synchronicity of each command,
    # as well as (re)drawing the prompt.

    @classmethod
    def evaluateCommand(self, actor, name, subcmd, argstr):
        peer = actor.peer
        if peer is not None:
            scope = getGirlPlayerScope(peer) # target of @dir()
            code = configuration.Interpreter.command_task or COMMAND_TASK

            try: program = Girl(Girl.Module, code + '\n')
            except GrammaticalError as e:
                print(f'{code}:')
                print(e.report())
            else:
                self.evaluateCode(peer, peer.interpreter, program, scope,
                                  tracing = getGirlTracingLevel(peer),
                                  subcommand = subcmd, command = name,
                                  arguments = argstr,
                                  this = PeerAdapter(peer),
                                  me = MobileAdapter(actor))

    @classmethod
    def evaluateVerb(self, peer, actor, command, argstr):
        scope = getGirlPlayerScope(peer) # target of @dir()
        code = configuration.Interpreter.verb_task or VERB_TASK

        try: program = Girl(Girl.Module, code + '\n')
        except GrammaticalError as e:
            print(f'{code}:')
            print(e.report())
        else:
            # A command that has entered evaluate-verb mode has abandoned all
            # hope of getting output any time soon (before the end of this
            # heartbeat), because evaluateCode initiates a new asynchronous task.
            peer.hasPrompt = True # If a command doesn't generate any output, it must set this false.

            task = self.evaluateCode(peer, peer.interpreter, program, scope,
                                     command = command,
                                     arguments = argstr,
                                     this = PeerAdapter(peer),
                                     me = MobileAdapter(actor))

            if task is not None:
                @task.onComplete
                def completion(_, exception = None):
                    if exception is None:
                        try: outcome = task.stack.pop()[0]
                        except IndexError: pass # Shouldn't happen
                        else: task.handleVerbOutcome(outcome, command, argstr)

                # Consider this command handled.
                return True


    @classmethod
    def evaluateEvent(self, peer, code, tracing = False, **environ):
        scope = getGirlPlayerScope(peer)

        try: program = Girl(Girl.Module, code + '\n')
        except GrammaticalError as e:
            print(f'{code}:')
            print(e.report())
        else:
            task = self.evaluateCode(peer, peer.interpreter, program, scope,
                                     tracing = tracing, **environ)

            return True


    @classmethod
    def evaluateMethodCall(self, request, path, name, *args):
        # RPC.  See phsite.network.adapter.commands.doCallMethod alternatively.
        # todo: finish:
        #   instantiate self for task class
        #   interface with isFromSecureHost and request/peer
        #   integrate with SessionManager
        #   this came from mental.library.model.GirlCore.rpcCallMethod
        from stuphos.kernel import checkActiveTasks, Programmer, nullproc, getLibraryCore, protectedMemoryLoad

        # name = path[-1]
        # path = path[:-1]

        # Acquire programmer and task state.
        progr = Programmer.NONE
        if request.user is not None:
            checkActiveTasks(request.user)

            for player in request.user.default_players.all():
                progr = Programmer(player.player.player_name)
                break

        task = Script.Load(user = request.user)
        core = getLibraryCore(task)

        vm = runtime[runtime.System.Engine]
        args = protectedMemoryLoad(task, args)

        task += dict(procedure = nullproc(), programmer = progr)
        vm += task

        return callGirlMethod(core, task, path, name, *args) () # block.


    @classmethod
    def invokeTrigger(self, peer, program, tracing = False):
        scope = getGirlPlayerScope(peer)
        self.evaluateCode(peer, peer.interpreter, program, scope,
                          tracing = tracing,
                          player = MobileAdapter(peer.avatar),
                          trigger = TriggerAdapter(self))

AgentScript = PlayerScript

class GirlPlayerProgrammeTrigger(Programme, events.Trigger):
    # Dual function: as stored programme, and also as triggerable player event.
    class _Meta(Programme._Meta):
        Attributes = Programme._Meta.Attributes + ['tracing']

    def __init__(self, *args, **kwd):
        tracing = getKeyword(kwd, 'tracing')
        Programme.__init__(self, *args, **kwd)
        self.tracing = tracing

    def __getstate__(self):
        state = Programme.__getstate__(self)
        state['tracing'] = self.tracing
        return state

    def getCompiledCode(self):
        if isinstance(self.sourceCode, str):
            # Compile as module.
            return Girl(Girl.Module, self.sourceCode) # self.source.replace('\r', '')

    getTriggerCode = getCompiledCode

    def invokeProgramme(self, shell, peer):
        code = self.getCompiledCode()
        scope = getGirlPlayerScope(peer)
        PlayerScript.evaluateCode(peer, shell, code, scope,
                                  tracing = self.tracing,
                                  player = peer.avatar,
                                  this = peer, me = peer.avatar)

    def invokeTrigger(self, player):
        PlayerScript.invokeTrigger(player.peer, self.getTriggerCode(),
                                   self.tracing)

class GirlCodeManager(ProgrammeManager):
    # ProgrammeManager:
    ProgrammeClass = GirlPlayerProgrammeTrigger

    def getManagerName(self):
        return 'Girl'
    def getManagerId(self):
        return '%s.%s.Instance' % (self.__class__.__module__, self.__class__.__name__)

class GirlCodeShell(EvaluationShell):
    # EvaluationShell:
    def executeGirl(self, shell, peer, argstr):
        return self.executeSourceCode(shell, peer, argstr)

    __call__ = executeGirl

    def executeCode(self, shell, peer, program):
        scope = self.getScope(peer)
        PlayerScript.evaluateCode(peer, shell, program, scope,
                                  tracing = self.tracing,
                                  player = peer.avatar,
                                  this = peer, me = peer.avatar)

    def compileSourceCodeBlock(self, peer, sourceCode):
        if isinstance(sourceCode, str):
            # Currently always is -- Compile as module.
            return Girl(Girl.Module, self.manager.formatSourceCode(sourceCode))

    def compileSingleStatement(self, peer, sourceCode):
        return Girl(Girl.Statement, self.manager.formatSourceCode(sourceCode))

    # Implementation.
    def __init__(self, manager, tracing = False):
        EvaluationShell.__init__(self, manager)
        self.tracing = tracing

    def getScope(self, peer):
        return getGirlPlayerScope(peer)

# Infrastructure.
def getVirtualMachine():
    from world import heartbeat as vm
    return vm

def getGirlScope(scope, name = None):
    # Basically return a persistant, shared namespace associated with,
    # wrapping, and being wrapped by the standard player scope.

    try: return scope.namespace
    except AttributeError: pass

    try: memory = scope.memory
    except AttributeError:
        memory = scope.memory = VM.Task.Memory.Connect(None) # XXX user = findUserByPrincipalName(name)

    ns = scope.namespace = VM.Task.Environment(memory)
    return ns

    # girl = getattr(scope, 'girl', Undefined)
    # if girl is Undefined:
    #     girl = new.module('%s.namespace' % Girl.__module__)

    #     # XXX UNSAFE.
    #     girl.shared = scope
    #     scope.girl = girl

    #     # Presumably, the girl-core facility is loaded before this is initialized.
    #     # XXX UNSAFE, because it exposes the core object to all player scripts.
    #     girl.core = runtime[runtime.Girl.System]

    # return girl.__dict__

# Singleton.
GirlCodeManager.Instance = GirlCodeManager()

def getGirlPlayerScope(peer):
    name = peer.avatar.name if peer.avatar else None
    return getGirlScope(getPlayerScope(peer), name = name)
def getGirlCodeEvaluator(*args, **kwd):
    return GirlCodeShell(GirlCodeManager.Instance, *args, **kwd)

class GirlCodeEvaluatorFactory(ShellFactoryBase):
    OPTIONS = [Option('-t', '--tracing', action = 'store_true')]

    def __new__(self, peer, tracing = False):
        print(EvaluationShell.PROGRAMMING_HEADER % 'Girl', file=peer)
        return getGirlCodeEvaluator(tracing)

def getGirlTracingLevel(peer):
    try: return peer.tracing
    except AttributeError:
        tracing = configuration.Interpreter.trace_commands
        if tracing == 'stack':
            return tracing

        return isYesValue(tracing)

def doGirlStatement(peer, cmd, argstr):
    # Execute single statement now.
    # todo: security policy
    if peer.avatar and peer.avatar.implementor:
        if argstr:
            # todo: delete_doubledollar(argstr)
            try:
                PlayerScript.evaluateStatement(peer, argstr, shell = peer.interpreter,
                                               tracing = getGirlTracingLevel(peer))
            except GrammaticalError as e:
                peer.sendln(e.report())

            return True

# Command Line.
def initCommands():
    try: from stuphmud.server.player import getSharedCommands # ...plain ACMD still being initialized.
    except ImportError: pass
    else: getSharedCommands().insertOverridingAll('@', doGirlStatement)

def createCommand(verb, path, commandName):
    def performGirlCommand(peer, cmd, argstr):
        from world import heartbeat as vm
        from stuphos.kernel import Script

        core = runtime[runtime.Agent.System]
        path = path.split('/')
        node = core.root.lookup(*path)
        task = Script() # Todo: PlayerScript import

        # Open subroutine and schedule.
        try: pos = node.module.symbols[commandName][0]
        except KeyError:
            raise NameError(commandName)

        # Todo: use string-name overload
        method = node.module.getSubroutine(pos)

        # todo: use executeGirl for synchronous option.
        task.addFrameCall(method, arguments = [cmd, argstr])
        vm += task
        return True

    from stuphmud.server.player import ACMD
    return ACMD(verb)(performGirlCommand)
