import time

import cv2

from opencv_gst_rtsp_server import OpenCVFrameRTSPServer

capture = cv2.VideoCapture("rtsp://example.com")
grabbed, frame = capture.read()
fps = int(capture.get(cv2.CAP_PROP_FPS))
fps = fps if  60 > fps > 0 else 30
duration = 1.0/fps 
height, width, channel = frame.shape

server = OpenCVFrameRTSPServer(width=width, height=height, channel=channel, fps=fps, use_h265=True, port=8001)
server.start_background()

while True:
    start_time = time.time()
    grabbed, frame = capture.read()
    if grabbed:
        server.set_frame(frame=frame)
    else:
       capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
       continue
    end_time = time.time()
    elapsed_time = end_time - start_time
    sleep_duration = duration - elapsed_time
    if sleep_duration > 0:
        time.sleep(sleep_duration)