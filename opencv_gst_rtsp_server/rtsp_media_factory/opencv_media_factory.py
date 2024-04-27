import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtsp', '1.0')
gi.require_version('GstRtspServer', '1.0')
from abc import abstractmethod

from gi.repository import Gst, GstRtsp, GstRtspServer

from ..exception.element_exception import ElementNotFoundException
from ..utils.gst_utils import GstUtilities

import logging
logger = logging.getLogger(__name__)


class OpenCVMediaFactory(GstRtspServer.RTSPMediaFactory):
    width: int
    height: int
    channel: int = 3
    fps: int 
    frame_num_dict: dict = {}
    frame = None
    pipeline: Gst.Element = None 
    use_gpu: bool = False
    use_h265: bool = False
    videoconvert: str = 'videoconvert ! video/x-raw,format=I420'
    encoder: str = 'x264enc'
    rtppay: str = 'rtph264pay config-interval=1 name=pay0 pt=96'
    format: str = 'BGR'
    def __init__(self, **properties):
        super(OpenCVMediaFactory, self).__init__(**properties)


    @abstractmethod
    def on_need_data(self, src, length: int):
        pass

    def stop(self):
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)

    def do_create_element(self, url: GstRtsp.RTSPUrl):
        self.src_format = 'BGR' if self.channel == 3 else 'BGRx'
        if self.use_gpu:
            if GstUtilities.is_element_exist(element_name='nvvideoconvert'):
                gpu_videoconvert_element_name = 'nvvideoconvert'
            elif GstUtilities.is_element_exist(element_name='nvvidconv'):
                # NguyenNH: nvvidconv doesn't support 3 channel so have to use videoconvert to convert to 4 channel:
                if self.channel == 3:
                    gpu_videoconvert_element_name = 'videoconvert ! video/x-raw,format=BGRx ! nvvidconv'
                else:
                    gpu_videoconvert_element_name = 'nvvidconv'
            else:
                raise ElementNotFoundException(element_name='nvvideoconvert, nvvidconv')
            
            self.videoconvert: str = f'{gpu_videoconvert_element_name} ! video/x-raw(memory:NVMM),format=I420'
            
            self.encoder: str = 'nvv4l2h265enc' if self.use_h265 else 'nvv4l2h264enc'
            if not GstUtilities.is_element_exist(element_name=self.encoder):
                raise ElementNotFoundException(element_name=self.encoder)
        else:
            self.videoconvert: str = 'videoconvert ! video/x-raw,format=I420'
            self.encoder: str = 'x265enc' if self.use_h265 else 'x264enc'

        self.rtppay = 'rtph265pay config-interval=1 name=pay0 pt=102' if self.use_h265 else 'rtph264pay config-interval=1 name=pay0 pt=96'

        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                    f'caps=video/x-raw,format={self.src_format},width={self.width},height={self.height},framerate={self.fps}/1 ' \
                    f'! {self.videoconvert} ' \
                    f'! {self.encoder} ' \
                    f'! {self.rtppay} '

        logger.debug(f"launch_string = {self.launch_string}")
        self.pipeline = Gst.parse_launch(self.launch_string)
        return self.pipeline

    def do_configure(self, rtsp_media: GstRtspServer.RTSPMedia):
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        self.frame_num_dict[appsrc] = 0
        appsrc.connect('need-data', self.on_need_data)
