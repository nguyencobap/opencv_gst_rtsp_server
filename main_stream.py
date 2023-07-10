from rtsp_server.opencv_stream_rtsp_server import OpenCVStreamRTSPServer
import time

server = OpenCVStreamRTSPServer(stream_link="rtsp://rtspstream.com/ball", port=8001)
server.start_background()

# Keep app run
while True:
    time.sleep(10)