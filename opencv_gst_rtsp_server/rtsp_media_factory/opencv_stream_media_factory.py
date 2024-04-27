import cv2
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtsp, GstRtspServer

from .opencv_media_factory import OpenCVMediaFactory

import logging
logger = logging.getLogger(__name__)


class OpenCVStreamMediaFactory(OpenCVMediaFactory):
    def __init__(self, stream_link: str, channel: int = 3, use_gpu: bool = False, use_h265: bool = False, **properties):
        super(OpenCVStreamMediaFactory, self).__init__(**properties)
        if stream_link.isnumeric():
            self.stream_link = int(stream_link)
        else:
            self.stream_link = stream_link
        self.use_gpu = use_gpu
        self.use_h265 = use_h265
        self.cap = cv2.VideoCapture(self.stream_link)

        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.width = self.width if self.width > 0 else 1920

        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.height = self.height if self.height > 0 else 1080

        self.channel = channel
        
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.fps = self.fps if  60 > self.fps > 0 else 30

        self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        logger.debug(f"self.width = {self.width}, self.height = {self.height}, self.channel = {self.channel}, self.fps = {self.fps}, self.duration = {self.duration}")

     
    def on_need_data(self, src, length: int):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                data = frame.tostring()
                buf = Gst.Buffer.new_allocate(None, len(data), None)
                buf.fill(0, data)
                buf.duration = self.duration
                timestamp = self.frame_num_dict[src] * self.duration
                buf.pts = buf.dts = int(timestamp)
                buf.offset = timestamp
                self.frame_num_dict[src] += 1
                retval = src.emit('push-buffer', buf)
                logger.debug('pushed buffer, frame {}, duration {} ns, durations {} s'.format(self.frame_num_dict[src],
                                                                                       self.duration,
                                                                                       self.duration / Gst.SECOND))
                if retval != Gst.FlowReturn.OK:
                    logger.debug(retval)
