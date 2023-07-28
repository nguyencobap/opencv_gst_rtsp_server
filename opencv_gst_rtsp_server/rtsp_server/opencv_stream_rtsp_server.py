
from opencv_gst_rtsp_server.rtsp_media_factory.opencv_stream_media_factory import OpenCVStreamMediaFactory
from opencv_gst_rtsp_server.rtsp_server.opencv_rtsp_server import OpenCVRTSPServer

class OpenCVStreamRTSPServer(OpenCVRTSPServer):
    def __init__(self, stream_link: str, port: int, endpoint: str = "/stream", **properties):
        factory = OpenCVStreamMediaFactory(stream_link=stream_link)
        super(OpenCVStreamRTSPServer, self).__init__(factory=factory, endpoint=endpoint, port=port, **properties)