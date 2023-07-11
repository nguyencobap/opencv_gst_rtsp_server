import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject
from utils.network_utils import NetworkUtils
from rtsp_media_factory.opencv_media_factory import OpenCVMediaFactory
from exception.network_exception import PortAlreadyInUseException
from threading import Thread
from utils.log_utils import logger

class OpenCVRTSPServer(GstRtspServer.RTSPServer):
    thread: Thread = None
    main_loop: GObject.MainLoop = None
    factory: OpenCVMediaFactory = None

    def __init__(self, port: int, **properties):
        super(OpenCVRTSPServer, self).__init__(**properties)
        if NetworkUtils.is_port_in_use(port=port):
            raise PortAlreadyInUseException(port=port)
        self.set_service(str(port))
        self.attach(None)

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