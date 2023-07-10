import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject
from utils.network_utils import NetworkUtils
from exception.network_exception import PortAlreadyInUseException
from threading import Thread

class OpenCVRTSPServer(GstRtspServer.RTSPServer):
    thread: Thread = None

    def __init__(self, port: int, **properties):
        super(OpenCVRTSPServer, self).__init__(**properties)
        if NetworkUtils.is_port_in_use(port=port):
            raise PortAlreadyInUseException(port=port)
        self.set_service(str(port))
        self.attach(None)

    def start(self):
        GObject.threads_init()
        Gst.init(None)

        loop = GObject.MainLoop()
        loop.run()

    def start_background(self) -> Thread:
        self.thread = Thread(target=self.start)
        self.thread.setDaemon(True)
        self.thread.start()
        return self.thread