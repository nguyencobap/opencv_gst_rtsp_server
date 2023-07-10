
from rtsp_media_factory.opencv_stream_media_factory import OpenCVStreamMediaFactory
from rtsp_server.opencv_rtsp_server import OpenCVRTSPServer

class OpenCVStreamRTSPServer(OpenCVRTSPServer):
    def __init__(self, stream_link: str, port: int, endpoint: str = "/stream", **properties):
        super(OpenCVStreamRTSPServer, self).__init__(port=port, **properties)
        self.factory = OpenCVStreamMediaFactory(stream_link=stream_link)
        self.factory.set_shared(True)
        self.get_mount_points().add_factory(endpoint, self.factory)
