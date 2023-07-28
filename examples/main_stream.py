from opencv_gst_rtsp_server import OpenCVStreamRTSPServer
import time

server = OpenCVStreamRTSPServer(stream_link="rtsp://admin:abcd1234@14.241.65.181", port=8001)
server.start_background()

# Keep app run
while True:
    time.sleep(10)