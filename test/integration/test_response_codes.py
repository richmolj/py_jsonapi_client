from ..fixtures import *
from ..helpers import *
import py_jsonapi_client as japi

class TestResponseCodes(object):

    @raises(japi.ServerError)
    def test_server_error_on_500(self):
        ResponseCode.where({ 'code': 500 }).all()

    @raises(japi.AccessDeniedError)
    def test_server_error_on_403(self):
        ResponseCode.where({ 'code': 403 }).all()
