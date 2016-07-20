import py_jsonapi_client as japi
import logging
import os

if os.environ.get('DEBUG') == 'true':
    japi.logger.setLevel(logging.DEBUG)
else:
    japi.logger.setLevel(logging.WARN)
