import logging
import sys
import os
logger = logging.getLogger('py_jsonapi_client')

# If running in console, log to STDOUT
if os.isatty(sys.stdin.fileno()):
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(stream_handler)
    logger.propagate = False
