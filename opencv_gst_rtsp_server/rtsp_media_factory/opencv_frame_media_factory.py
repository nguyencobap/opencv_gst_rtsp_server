import gi

from .opencv_media_factory  import OpenCVMediaFactory

gi.require_version('Gst', '1.0')
from gi.repository import Gst

import logging
logger = logging.getLogger(__name__)

class OpenCVFrameMediaFactory(OpenCVMediaFactory):
    def __init__(self, width: int, height: int, fps: int, channel: int = 3, use_gpu: bool = False, use_h265: bool = False, **properties):
        super(OpenCVFrameMediaFactory, self).__init__(**properties)
        self.width = width
        self.height = height
        self.channel = channel
        self.fps = fps
        self.use_gpu = use_gpu
        self.use_h265 = use_h265
        self.frame = None
        self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        logger.debug(f"self.width = {self.width}, self.height = {self.height}, self.channel = {self.channel}, self.fps = {self.fps}, self.duration = {self.duration}")

    def set_frame(self, frame):
        self.frame = frame

    def on_need_data(self, src, length: int):
        if self.frame is not None:
            data = self.frame.tostring()
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
