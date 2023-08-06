from Commacceslib.use_comm import UseBridge
from PBaccesslib.hearbeat_thread import KillableThread


class CommBridge:
    """ Main ProbeCard class"""

    def __init__(self, ip, sync, _async, libpath):
        self._bridge = self._init_library_connection(ip, sync, _async, libpath)

    def _init_library_connection(self, ip, sync, _async, libpath):
        """"""
        self._bridge = UseBridge(ip, sync, _async, libpath)
        self.heartbeat = KillableThread(self._bridge.use_update_HB, sleep_interval=2.5)
        self.heartbeat.start()
        return self._bridge

    def touch_down(self):
        """"""
        return self._bridge.use_read_touchdown()

    def close_connection(self):
        """ Close the comunication with the library """
        self._bridge.close_communication()

    def kill_hearbeat(self):
        """"""
        self.heartbeat.kill()

    def return_bridge(self):
        """"""
        return self._bridge
