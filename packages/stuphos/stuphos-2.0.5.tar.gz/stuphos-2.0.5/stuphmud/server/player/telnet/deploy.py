# Deployment Telnet Dispatch Module
from stuphmud.server.player.db.managedfs import getCheckedPlayerFilename, PERSONAL_PLRFILE_DIR
from stuphmud.server.player.telnet import DispatchModuleBase

deploymentApi = runtime.MUD.Deployment.API
class LiveDeployDispatchModule(DispatchModuleBase):
    MULTITHREAD = True

    class PlayerFileArchive(deploymentApi.getArchiveBaseClass()):
        def __init__(self, peer, archive_name):
            plrfile = getCheckedPlayerFilename(peer, archive_name, PERSONAL_PLRFILE_DIR)
            FileArchive.__init__(self, plrfile, archive_name)

    class WizardProgress(deploymentApi.getProgressStreamBaseClass()):
        EOL = '\r\n'

        def __init__(self, player, synchronize):
            ProgressStream.__init__(player, synchronize)
            self.player = player

        def getStream(self):
            # This way, the player can be updated even if the connection re-logs in!
            return self.player.peer

    def _doDeployPersonalArchive(self, peer, digest, config_name, archive_name, update_message = None):
        config = deploymentApi.LoadDeploymentConfig(config_name)

        # todo: lock on config -- to prevent overlapping deploy conflicts
        if self._validateMessage(digest, config.key, peer.avatar.name, config_name, archive_name):
            deploymentApi.LiveDeploymentUrlFromConfigAndArchiveOnMultithread \
                (self.MULTITHREAD, config, self.PlayerFileArchive(peer, archive_name),
                 updateMessage = update_message)
                # progress_proc = self.WizardProgress(peer.player, self.MULTITHREAD)

    _doDeploypersonalarchive = _doDeployPersonalArchive
    _doDeploy = _doDeployPersonalArchive
