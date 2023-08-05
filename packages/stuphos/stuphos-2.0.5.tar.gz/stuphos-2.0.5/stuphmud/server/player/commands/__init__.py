# Player Commands Package.
from stuphmud.server.player import ACMD, ACMDLN, Option, getSharedScope
from stuphos.etc.tools import logException
from .mime import loadMessageFile
from os import listdir
from os.path import join as joinpath
import string

def installCommands():
    from stuphos.management.services import getEnablingSection
    isEnabled = getEnablingSection('Interpreter')

    if isEnabled('rich-editor'):
        import stuphmud.server.player.editor
    if isEnabled('player-notebook'):
        import stuphmud.server.player.notebook

    if isEnabled('wizard-gc'):
        from stuphmud.server.player.commands.gc import wizard
    if isEnabled('checkpointing'):
        from stuphmud.server.player.commands.gc import system
        system.EnableCheckpointing()

    try: loadFilesystemCommands()
    except: logException(traceback = True) # Is this right here?

def loadFilesystemCommands():
    from stuphos import getSection
    commands = getSection('VerbCommands')

    # Define commands from files in folder.
    for option in commands.options():
        if option.startswith('commands-folder'):
            folder = commands.get(option)
            for filename in listdir(folder):
                if filename.endswith('.mime'):
                    filename = joinpath(folder, filename)
                    with open(filename) as message:
                        loadMessageFile(message)

# Todo: Runtime API.
class BuiltCommandError(SyntaxError):
    def __init__(self, syntax, declaration, tb):
        self.syntax = syntax
        self.declaration = declaration
        self.tb = tb

def programVerbCommand(verbCode, language, source, options = [],
                       minlevel = None, group = None,
                       shlex = None, decorators = []):

    assert language == 'python'

    # Format parameters and verb name.
    parameters = 'player, command'

    if '*' not in verbCode:
        verbCode += '*'

    # Make command registrator.
    register = ACMDLN(verbCode,
                      *(options or []),
                      **dict(shlex = shlex))

    # Decide function name holding command code.
    valid = string.lowercase + string.uppercase + string.digits

    def formatWord(w):
        # Strip invalid characters.
        w = ''.join(c for c in w if c in valid)
        return w[:1].upper() + w[1:].lower()

    functionName = verbCode.replace('_', '-').split('-')
    functionName = 'do%s' % ''.join(formatWord(w) for w in functionName)

    def buildCommand(functionName, parameters, statements):
        # Compile the command statements and return the function.
        statements = statements.replace('\r', '')
        declaration = 'def %s(%s):\n    %s\n' % \
                       (functionName, parameters,
                        '\n    '.join(statements.split('\n')))

        # Declare function symbol in locals, but bind it to a
        # shared global scope so it has access later.
        ns = dict()

        # scope = player.interpreter.scope.__dict__

        ##    from mud.player import getPlayerScope
        ##    scope = getPlayerScope(player).__dict__

        scope = getSharedScope().__dict__

        try: exec(declaration, scope, ns)
        except SyntaxError as syntax:
            from sys import exc_info
            (_, _, tb) = exc_info()
            raise BuiltCommandError(syntax, declaration, tb)

        return ns[functionName]

    # Perform build.
    function = buildCommand(functionName, parameters, source)

    # Wrap.
    for d in decorators:
        function = d(function)

    register(function)
    return function
