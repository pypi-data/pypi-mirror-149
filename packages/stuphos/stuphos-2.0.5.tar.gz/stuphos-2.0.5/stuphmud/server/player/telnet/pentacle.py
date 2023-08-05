# Pentacle Command -- Telnet Dispatch Module.
#
from stuphos.runtime import Object, Synthetic
from stuphos.etc.tools import getSystemException
from stuphmud.server.player import HandleCommandError
from stuphmud.server.player.telnet.dispatch import DispatchModuleBase

pentacle = runtime.Pentacle.Module(__import__, 'pentacle')
telnetDispatchApi = runtime[runtime.Telnet.Dispatch.API]

@telnetDispatchApi.RegisterModuleClass('pentacle')
class PentacleDispatchModule(DispatchModuleBase):
    class _doCommand(object):
        def __init__(self, peer):
            # This class is supposed to act as a wrapper to the peer,
            # as well as dispatch the pentacle command.
            self.peer = peer

        def __new__(self, instance, peer, package):
            this = object.__new__(self)
            this.__init__(peer)

            cmd = pentacle.packaging.Command.FromPackage(package, this.dataChannel)
            return this(cmd)

        # Accessors
        dataChannel = property(lambda self:self.framework.dataChannel)
        mode = property(lambda self:self.framework.mode)

        @property
        def framework(self):
            a = self.peer.avatar
            try: f = a.framework
            except AttributeError:
                f = a.framework = Synthetic()

            try: return f.pentacle
            except AttributeError:
                p = f.pentacle = self.Framework(self)
                return p

        # Invocation Routine
        def __call__(self, cmd):
            try: response = self.mode.invokeCommand(cmd.command, *cmd.args, **cmd.kwd)
            except: self.handleCommandException(cmd.serialId, getSystemException())
            else: self.handleCommandResponse(cmd.serialId, response)

        def handleCommandResponse(self, serialId, response):
            self.peer.avatar('say %s' % response)
        def handleCommandException(self, serialId, excInfo):
            HandleCommandError(self.peer, excInfo, frame_skip = 0)

        class Framework(Object):
            def __init__(self, dispatch):
                self.dispatch = dispatch
                self.dataChannel = pentacle.encoding.EntitySpace()
                self.mode = self

            def invokeCommand(self, name, *args, **kwd):
                # Application layer.  For now, just return a string describing call.
                # (this could, say, lookup objects off of a scope-chain within this
                #  framework).
                #
                # Obviously this is a great entry-point for O-O P2P RPC with a Girl
                # evaluator.
                return '%s%s%s%s%s' % (name, (args or kwd) and ' ' or '',
                                       ', '.join(map(str, args)),
                                       args and kwd and ', ' or '',
                                       ', '.join('%s = %r' % nv for nv in \
                                                 kwd.items()))
