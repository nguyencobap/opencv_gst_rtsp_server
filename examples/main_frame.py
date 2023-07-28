from opencv_gst_rtsp_server import OpenCVFrameRTSPServer
import cv2

capture = cv2.VideoCapture("rtsp://admin:abcd1234@14.241.65.181")
grabbed, frame = capture.read()
fps = int(capture.get(cv2.CAP_PROP_FPS))
fps = fps if  60 > fps > 0 else 30
height, width, channels = frame.shape

server = OpenCVFrameRTSPServer(width=width, height=height, fps=fps, port=8001)
server.start_background()

while True:
    grabbed, frame = capture.read()
    server.set_frame(frame=frame)
    if not grabbed:
        break