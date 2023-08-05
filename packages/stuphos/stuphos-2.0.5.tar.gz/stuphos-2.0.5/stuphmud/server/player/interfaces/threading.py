import _thread
from stuphmud import server as mud

from pprint import pprint
class ThreadingManager:
    def enqueueHeartbeatTask(self, peer, task, *args, **kwd):
        'Manages the creation/destruction/start/stop of the private shell heartbeat task instance and its messaging.'

        import world
        world.heartbeat.enqueueHeartbeatTask(self.withPeerHead, peer, task, *args, **kwd)

    def spawnTask(self, peer, task, *args, **kwd):
        '''
        spawn(<peer>, <task>, *args, **kwd)

        Processes a <task - 2nd arg> with *args and **kwd IN A SEPARATE THREAD.
        It posts the result to the heartbeat task by handling it in that context.

        If there's an error in the task (exception), show that to the player in
        the heartbeat thread.

        If the task succeeds, show the result to the player in the heartbeat.

        '''

        from sys import exc_info

        # wraps output/result/exception/toplevel in peer head anchored in heartbeat.
        def handleError(exc):
            mud.player.HandleCommandError(peer, exc)

        def handleResult(result):
            if result is not None:
                if type(result) is str:
                    peer.page(result)

                else:
                    try   : pprint(result, peer)
                    except: mud.player.HandleCommandError(peer, exc_info())

        def taskReport(task, args, kwd):
            # Thread tasks - processes invocation and posts an event task as response.
            try   : ev = handleResult, task    (*args, **kwd)
            except: ev = handleError,  exc_info(            )

            import world
            world.heartbeat.enqueueHeartbeatTask(*ev)

        return _thread.start_new_thread(taskReport, (task, args, kwd))
