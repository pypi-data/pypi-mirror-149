import logging
import os
import sys

# sys.path.append('../../')

# PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.getcwd()
PATH = os.path.join(PATH, '../log/client.log')

logger = logging.getLogger('app.client_script')
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s ")
file_handler = logging.FileHandler(PATH, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)
