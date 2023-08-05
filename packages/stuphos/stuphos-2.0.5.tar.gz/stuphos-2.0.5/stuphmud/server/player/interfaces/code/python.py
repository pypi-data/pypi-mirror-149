# Python Code Shell Evaluator.
import stuphos
from stuphmud import server as mud
from stuphos.etc.tools import getSystemException, Attributes
from stuphmud.server.player import HandleCommandError, policy, getPlayerScope
from stuphmud.server.player.interfaces.code import ShellFactoryBase
from . import ProgrammeManager, EvaluationShell, TemporaryCodeFile, isFromSecureHost

@Attributes.Dynamic
def Environment(player, name, **search):
    return player.find(name, **search)

class PythonCodeManager(ProgrammeManager):
    # ProgrammeManager:
    def getManagerName(self):
        return 'Python'
    def getManagerId(self):
        return '%s.%s.Instance' % (self.__class__.__module__, self.__class__.__name__)

    # Implementation.
    isFromSecureHost = staticmethod(isFromSecureHost)
    def isPythonAllowed(self, peer):
        # Connection must originate from this machine.
        if not self.isFromSecureHost(peer):
            return False

        avatar = peer.avatar
        if avatar:
            if avatar in policy:
                # Powerful.
                return True

            # This line allows all implementors to use python:
            return avatar.supreme

        return False

    PROLOG = 'from __future__ import with_statement\n'
    EPILOG = ''

    def getDefaultShellName(self):
        # (code source)
        return '?'

    def compileSourceCodeBlock(self, peer, sourceCode, shellName = None):
        # Remove-preceding whitespace.
        sourceCode = self.formatSourceCode(sourceCode.lstrip())
        sourceCode = ''.join((self.PROLOG, sourceCode, self.EPILOG))

        if shellName is None:
            shellName = self.getDefaultShellName()

        # Compile code from source.
        with TemporaryCodeFile(peer, sourceCode, shellName):
            return compile(sourceCode, shellName, 'exec')

    def compileSingleStatement(self, peer, sourceCode, shellName = None):
        if shellName is None:
            shellName = self.getDefaultShellName()

        sourceCode = self.formatSourceCode(sourceCode)
        with TemporaryCodeFile(peer, sourceCode):
            return compile(sourceCode, shellName, 'single')

    def executeCode(self, shell, peer, code, **environ):
        # Hack: inspect evaluator stack on CodeManager Shell.
        managerName = self.getManagerName()

        try: execute = shell.getEvaluatorByManagerName(managerName).executeCode
        except AttributeError: pass
        else: return execute(shell, peer, code, **environ)

class PythonCodeShell(EvaluationShell):
    # EvaluationShell:
    def executePython(self, shell, peer, argstr):
        if argstr and self.manager.isPythonAllowed(peer):
            return self.executeSourceCode(shell, peer, argstr)

    __call__ = executePython

    def executeCode(self, shell, peer, code, **environ):
        local = self.setupLocalNamespace(shell, peer, (None, None), **environ)

        ##    if getattr(self, 'debug', False):
        ##        debug_code(code, local)

        try: exec(code, self.global_namespace, local)
        except:
            # For now, show all how we got here.
            HandleCommandError(peer, getSystemException(), frame_skip = 0)

    # Implementation.
    thisName   = 'this' # avatar's peer
    myName     = 'me'   # peer's avatar
    myLocation = 'here' # avatar's room location

    shellName  = '<player>'

    def __init__(self, manager, scope):
        EvaluationShell.__init__(self, manager)
        self.scope = scope

        # I guess these are separately-configurable.
        self.local_namespace = scope.__dict__
        self.global_namespace = getMainNamespace(scope)

    def getShellName(self, peer):
        'Code Source (not source code).'

        self.compiler_name = shellName = getattr(peer, 'host', False) or self.shellName
        return shellName

    def compileSourceCodeBlock(self, peer, sourceCode):
        return self.manager.compileSourceCodeBlock(peer, sourceCode, self.getShellName(peer))
    def compileSingleStatement(self, peer, sourceCode):
        return self.manager.compileSingleStatement(peer, sourceCode, self.getShellName(peer))

    def setupLocalNamespace(self, shell, peer, xxx_todo_changeme, **environ):
        (cmd, argstr) = xxx_todo_changeme
        local = self.local_namespace
        avatar = peer.avatar

        local.update({
            self.thisName   : peer,
            self.myName     : avatar or peer.avatar,
            self.myLocation : avatar and avatar.room,

            # '__command__'   : cmd,
            # '__argstr__'    : argstr,

            'commands'      : shell.commands,
            'acmd'          : getattr(shell.commands, 'insert', None), # or just self.insert
            'history'       : shell.historyObject(peer),
            'last'          : lambda *args, **kwd:shell.historyLast(peer, *args, **kwd),

            'sh'            : shell,
            'run'           : shell.enqueueHeartbeatTask,
            'spawn'         : shell.spawnTask,
            'inline'        : stuphos.enqueueHeartbeatTask,

            'e'             : Environment(avatar),
            'g'             : Environment(avatar, mobile_in_world = True, item_in_world = True),

            # 'com'           : self.getCode,
        })

        local.update(environ)
        return local

# Infrastructure.
def getMainNamespace(scope):
    main = getModule()
    main.shell = scope
    main.main = main

    from stuphmud import server as mud
    import pdb
    main.mud = mud
    main.pdb = pdb

    from stuphos.system.api import game, world
    main.game = game
    main.world = world

    import builtins as builtin
    main.builtin = builtin

    import sys, os
    main.sys = sys
    main.os = os

    return main.__dict__

def getModule(name = '__main__'):
    # This should go in tools.

    try: main = __import__(name)
    except ImportError:
        main = new.module(name)
        from sys import modules
        modules[name] = main

    return main

# Singleton.
PythonCodeManager.Instance = PythonCodeManager()

def getPythonCodeEvaluator(scope):
    return PythonCodeShell(PythonCodeManager.Instance, scope)

class PythonCodeEvaluatorFactory(ShellFactoryBase):
    def __new__(self, peer):
        print(EvaluationShell.PROGRAMMING_HEADER % 'Python', file=peer)
        return getPythonCodeEvaluator(getPlayerScope(peer))
