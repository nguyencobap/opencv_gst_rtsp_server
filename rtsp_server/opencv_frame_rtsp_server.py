
from rtsp_media_factory.opencv_frame_media_factory import OpenCVFrameMediaFactory
from rtsp_server.opencv_rtsp_server import OpenCVRTSPServer

class OpenCVFrameRTSPServer(OpenCVRTSPServer):
    def __init__(self, width: int, height: int, fps: int, port: int, endpoint: str = "/stream", **properties):
        super(OpenCVFrameRTSPServer, self).__init__(port=port, **properties)
        self.factory = OpenCVFrameMediaFactory(width=width, height=height, fps=fps)
        self.factory.set_shared(True)
        self.get_mount_points().add_factory(endpoint, self.factory)

    def set_frame(self, frame):
        self.factory.set_frame(frame=frame)