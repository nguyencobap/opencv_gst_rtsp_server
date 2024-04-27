import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject
from ..utils.network_utils import NetworkUtils
from ..rtsp_media_factory.opencv_media_factory import OpenCVMediaFactory
from ..exception.network_exception import PortAlreadyInUseException
from threading import Thread
from ..utils.thread_utils import ThreadUtilities

import logging
logger = logging.getLogger(__name__)

class OpenCVRTSPServer(GstRtspServer.RTSPServer):
    thread: Thread = None
    main_loop: GObject.MainLoop = None
    server_id: int
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

    def get_port(self) -> int:
        return self.port
    
    def get_endpoint(self) -> str:
        return self.endpoint

    def start(self):
        if self.main_loop is None or not self.main_loop.is_running():
            GObject.threads_init()
            Gst.init(None)

            self.main_loop = GObject.MainLoop()
            self.server_id = self.attach(self.main_loop.get_context())
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
        
        GObject.source_remove(self.server_id)

        if self.thread:
            try:
                ThreadUtilities.async_raise(self.thread.ident)
            except:
                logger.error("Stop thread failed", exc_info=True)
        else:
            logger.debug("self.thread null")