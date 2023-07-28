import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject
from opencv_gst_rtsp_server.utils.network_utils import NetworkUtils
from opencv_gst_rtsp_server.rtsp_media_factory.opencv_media_factory import OpenCVMediaFactory
from opencv_gst_rtsp_server.exception.network_exception import PortAlreadyInUseException
from threading import Thread
from opencv_gst_rtsp_server.utils.log_utils import logger

class OpenCVRTSPServer(GstRtspServer.RTSPServer):
    thread: Thread = None
    main_loop: GObject.MainLoop = None
    factory: OpenCVMediaFactory = None
    endpoint: str = "/stream"
    port: int

    def __init__(self, factory: OpenCVMediaFactory, port: int, endpoint: str = "/stream", **properties):
        super(OpenCVRTSPServer, self).__init__(**properties)
        self.endpoint = endpoint
        self.port = port
        self.factory = factory

        if NetworkUtils.is_port_in_use(port=self.port):
            raise PortAlreadyInUseException(port=self.port)
        self.set_service(str(self.port))

        self.factory.set_shared(True)
        self.get_mount_points().add_factory(self.endpoint, self.factory)
        self.attach(None)

    def get_port(self) -> int:
        return self.port
    
    def get_endpoint(self) -> str:
        return self.endpoint

    def start(self):
        if self.main_loop is None or not self.main_loop.is_running():
            GObject.threads_init()
            Gst.init(None)

            self.main_loop = GObject.MainLoop()
            self.main_loop.run()
        else:
            logger.debug("Main loop has already been run")

    def start_background(self) -> Thread:
        if self.thread is None or not self.thread.is_alive():
            self.thread = Thread(target=self.start)
            self.thread.setDaemon(True)
            self.thread.start()
        else:
            logger.debug("Thread has already been started")
        return self.thread
    
    def stop(self):
        if self.factory:
            self.factory.stop()
        else:
            logger.debug("Factory is None")

        if self.main_loop and self.main_loop.is_running():
            self.main_loop.quit()
        else:
            logger.debug("Main loop has already been quit")