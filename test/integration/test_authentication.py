from ..fixtures import *
from ..helpers import *
import py_jsonapi_client as japi

class TestAuthentication(object):
    @raises(japi.UnauthenticatedError)
    def test_unauthenticated_request_raises(self):
        admin = Admin.first()

    def test_authenticated_request(self):
        admin = AuthdAdmin.first()
        assert admin.name == 'joe admin'
