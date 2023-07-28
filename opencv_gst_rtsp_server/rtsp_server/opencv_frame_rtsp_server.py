
from opencv_gst_rtsp_server.rtsp_media_factory.opencv_frame_media_factory import OpenCVFrameMediaFactory
from opencv_gst_rtsp_server.rtsp_server.opencv_rtsp_server import OpenCVRTSPServer

class OpenCVFrameRTSPServer(OpenCVRTSPServer):
    def __init__(self, width: int, height: int, fps: int, port: int, endpoint: str = "/stream", **properties):
        factory = OpenCVFrameMediaFactory(width=width, height=height, fps=fps)
        super(OpenCVFrameRTSPServer, self).__init__(factory=factory, endpoint=endpoint, port=port, **properties)

    def set_frame(self, frame):
        self.factory.set_frame(frame=frame)