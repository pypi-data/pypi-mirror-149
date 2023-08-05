# MUD . Player . Interfaces
# todo: rename to mud.interface.shell
from stuphmud import server as mud
from . import dictcmd

class ACMD:
    Name = '?'
    def __init__(self, **kwd):
        self.__dict__.update(kwd)

class CommandCenter(dictcmd.CmdDict):
    # This can probably go away and just use CmdDict..?

    def __init__(self):
        dictcmd.CmdDict.__init__(self)
        self.setup()

    def setup(self):
        pass

    def importCommands(self, module):
        for proc in  __import__(module).__all__:
            if callable(proc) and hasattr(proc, 'ACMD'):
                self.insertAssignment(proc.ACMD.Name, proc)

def getCommandCenter(module):
    if not hasattr(module, 'SharedCommands'):
        from .standard import StandardCommands
        module.SharedCommands = StandardCommands()
        module.ACMD = module.assignCommand = module.SharedCommands.assign

    return module.SharedCommands

# Python implementation of a command manager that can execute verbs out of a dictionary.
class CommandManager:
    def __init__(self, commands = None):
        self.commands = commands

    # Fraun Dec 21st 2005 Incorporation of CmdDict
    def playerCommand(self, peer, cmd, argstr):
        # Fraun Oct 1st 2006 - Only playing connections for commands!
        if peer.avatar:
            # todo: mud.tasks.triggers.verbCommand

            action = self.commands.lookup(cmd)
            if callable(action):
                try: return action(peer, cmd, argstr)
                except (mud.player.PlayerResponse, mud.player.DoNotHere) as e:
                    print(e, file=peer) # e.message
                    return True

                except mud.player.PlayerAlert as e:
                    e.deliver(peer)
                    return True

    try: from world.commands import parseCommand
    except ImportError:
        def parseCommand(self, cmdln):
            return self.commands.parse(cmdln)

    def assignCommand(self, *args):
        return self.commands.insertOverridingAll(*args)

    def getCommands(self):
        return self.commands

from .history import HistoryManager
from .threading import ThreadingManager
from .code import CodeManager, makeCodeEvaluators
