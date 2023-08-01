import logging
import os

is_debug: bool = False
if 'OPENCV_GST_RTSP_SERVER_DEBUG' in os.environ:
    is_debug = os.environ['OPENCV_GST_RTSP_SERVER_DEBUG'].lower() == "true"

logger: logging.Logger = logging.getLogger('logger')
if is_debug:
    logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname).1s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)