import logging

logger: logging.Logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname).1s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)