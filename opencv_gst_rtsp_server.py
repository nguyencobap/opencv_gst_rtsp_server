import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject
from opencv_factory import OpenCVFactory
from utils.log_utils import logger
from utils.network_utils import NetworkUtils
from exception.network_exception import PortAlreadyInUseException

class OpenCVGstRTSPServer(GstRtspServer.RTSPServer):
    def __init__(self, stream_link: str, port: int, **properties):
        if NetworkUtils.is_port_in_use(port=port):
            raise PortAlreadyInUseException(port=port)
        super(OpenCVGstRTSPServer, self).__init__(**properties)
        self.factory = OpenCVFactory(stream_link=stream_link)
        self.factory.set_shared(True)
        self.get_mount_points().add_factory("/test", self.factory)
        self.set_service(str(port))
        self.attach(None)

    def start(self):
        GObject.threads_init()
        Gst.init(None)

        loop = GObject.MainLoop()
        loop.run()
