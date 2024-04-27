
from ..rtsp_media_factory.opencv_frame_media_factory import OpenCVFrameMediaFactory
from .opencv_rtsp_server import OpenCVRTSPServer


class OpenCVFrameRTSPServer(OpenCVRTSPServer):
    def __init__(self, width: int, height: int, fps: int, port: int, channel: int = 3, endpoint: str = "/stream", use_gpu: bool = False, use_h265: bool = False, **properties):
        factory = OpenCVFrameMediaFactory(width=width, height=height, channel=channel, fps=fps, use_gpu=use_gpu, use_h265=use_h265)
        super(OpenCVFrameRTSPServer, self).__init__(factory=factory, endpoint=endpoint, port=port, **properties)

    def set_frame(self, frame):
        self.factory.set_frame(frame=frame)