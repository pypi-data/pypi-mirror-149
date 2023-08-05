import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys

# sys.path.append('../../')

# PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.getcwd()
PATH = os.path.join(PATH, '../log/server.log')
logger = logging.getLogger('app.server_script')
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s ")
file_handler = TimedRotatingFileHandler(PATH, encoding='utf-8', interval=1, when='midnight')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)
