import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject
from opencv_factory import OpenCVFactory
from utils.log_utils import logger

class OpenCVGstRTSPServer(GstRtspServer.RTSPServer):
    def __init__(self, stream_link: str, port: int, **properties):
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
