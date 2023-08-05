# Remote Execution Telnet Module
from stuphmud.server.player.telnet import DispatchModuleBase
from stuphmud.server.player.telnet.dispatch import LoadKeyfile

from stuphmud.server.player import getPlayerScope, playerAlert
from stuphmud.server.player.db.managedfs import getCheckedPlayerFilename, KEYFILE_DIR, PERSONAL_PLRFILE_DIR

import os.path
from new import module as NewModule

class RExecDispatchModule(DispatchModuleBase):
    def validatePlayerCommandMessage(self, peer, digest, message):
        # XXX Should warn when the digest doesn't match?
        return self._validateMessage(digest, self.getPlayerKey(peer), peer.avatar.name, message)

    def getPlayerKey(self, peer):
        # Retrieve player key from personal file store.
        filename = getCheckedPlayerFilename(peer, 'rexec.key', KEYFILE_DIR)
        return LoadKeyfile(filename)

    def getPlayerId(self, peer):
        return '%s%s' % (peer.avatar.name, peer.avatar.idnum)

    def getScopeModule(self, peer):
        scope = getPlayerScope(peer)
        try: return scope.rexec
        except AttributeError:
            rexec = NewModule('%s.namespace' % __name__)
            scope.rexec = rexec
            return rexec

    def getPlayerScope(self, module, peer):
        try: scope = module.playerScope
        except AttributeError:
            scope = module.playerScope = {}

        playerId = self.getPlayerId(peer)
        try: return scope[playerId]
        except KeyError:
            playerMod = NewModule('%s.namespace.%s' % (__name__, playerId))
            scope[playerId] = playerMod
            return playerMod

    def getScope(self, peer):
        module = self.getScopeModule(peer)
        immediate = self.getPlayerScope(module, peer)

        # Install environment.
        immediate.this = peer
        immediate.me = peer.avatar

        return (module.__dict__, immediate.__dict__)

    def _doExecute(self, peer, digest, sourceCode):
        if self.validatePlayerCommandMessage(peer, digest, sourceCode):
            # Evaluator Shell?
            code = compile(sourceCode, '<rexec>', 'single')
            (globals, locals) = self.getScope(peer)

            def executeCode(peer):
                exec(code, globals, locals)

            peer.interpreter.withPeerHead(peer, executeCode)

    def _doExecuteFile(self, peer, digest, filename):
        if self.validatePlayerCommandMessage(peer, digest, filename):
            plrfile = getCheckedPlayerFilename(peer, filename, PERSONAL_PLRFILE_DIR)
            sourceCode = open(plrfile).read()
            sourceCode = sourceCode.replace('\r', '')
            code = compile(sourceCode, filename, 'exec')

            (globals, locals) = self.getScope(peer)
            globals['__file__'] = plrfile # filename

            def executeCode(peer):
                exec(code, globals, locals)

            peer.interpreter.withPeerHead(peer, executeCode)

    _doExecutefile = _doExecuteFile
