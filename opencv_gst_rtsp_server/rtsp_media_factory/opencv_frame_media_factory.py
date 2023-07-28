from opencv_gst_rtsp_server.utils.log_utils import logger
from opencv_gst_rtsp_server.rtsp_media_factory.opencv_media_factory import OpenCVMediaFactory
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

class OpenCVFrameMediaFactory(OpenCVMediaFactory):
    def __init__(self, width: int, height: int, fps: int, **properties):
        super(OpenCVFrameMediaFactory, self).__init__(**properties)
        self.number_frames = 0
        self.width = width
        self.height = height
        self.fps = fps
        self.frame = None
        self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        logger.debug(f"self.width = {self.width}, self.height = {self.height}, self.fps = {self.fps}, self.duration = {self.duration}")

    def set_frame(self, frame):
        self.frame = frame

    def on_need_data(self, src, length: int):
        if self.frame is not None:
            data = self.frame.tostring()
            buf = Gst.Buffer.new_allocate(None, len(data), None)
            buf.fill(0, data)
            buf.duration = self.duration
            timestamp = self.number_frames * self.duration
            buf.pts = buf.dts = int(timestamp)
            buf.offset = timestamp
            self.number_frames += 1
            retval = src.emit('push-buffer', buf)
            logger.debug('pushed buffer, frame {}, duration {} ns, durations {} s'.format(self.number_frames,
                                                                                    self.duration,
                                                                                    self.duration / Gst.SECOND))
            if retval != Gst.FlowReturn.OK:
                logger.debug(retval)
