import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GstRtsp
from opencv_gst_rtsp_server.utils.log_utils import logger
from abc import abstractmethod

class OpenCVMediaFactory(GstRtspServer.RTSPMediaFactory):
    width: int
    height: int
    fps: int 
    number_frames: int = 0
    frame = None
    pipeline: Gst.Element = None 
    def __init__(self, **properties):
        super(OpenCVMediaFactory, self).__init__(**properties)


    @abstractmethod
    def on_need_data(self, src, length: int):
        pass

    def stop(self):
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)

    def do_create_element(self, url: GstRtsp.RTSPUrl):
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                            f'caps=video/x-raw,format=BGR,width={self.width},height={self.height},framerate={self.fps}/1 ' \
                            '! videoconvert ! video/x-raw,format=I420 ' \
                            '! x264enc speed-preset=ultrafast tune=zerolatency ' \
                            '! rtph264pay config-interval=1 name=pay0 pt=96'
        self.pipeline = Gst.parse_launch(self.launch_string)
        return self.pipeline

    def do_configure(self, rtsp_media: GstRtspServer.RTSPMedia):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)


