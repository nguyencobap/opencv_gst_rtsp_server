
from ..rtsp_media_factory.opencv_stream_media_factory import OpenCVStreamMediaFactory
from .opencv_rtsp_server import OpenCVRTSPServer

class OpenCVStreamRTSPServer(OpenCVRTSPServer):
    def __init__(self, stream_link: str, port: int, endpoint: str = "/stream", use_gpu: bool = False, use_h265: bool = False, **properties):
        factory = OpenCVStreamMediaFactory(stream_link=stream_link, use_gpu=use_gpu, use_h265=use_h265)
        super(OpenCVStreamRTSPServer, self).__init__(factory=factory, endpoint=endpoint, port=port, **properties)