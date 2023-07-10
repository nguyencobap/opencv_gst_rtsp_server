from opencv_gst_rtsp_server import OpenCVGstRTSPServer

server = OpenCVGstRTSPServer(stream_link="rtsp://rtspstream.com/ball", port=8001)
server.start()