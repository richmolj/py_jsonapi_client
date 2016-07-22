from ..fixtures import *
from ..helpers import *
import py_jsonapi_client as japi

class TestDirtyTracking(object):

    def test_original_attributes_updated(self):
        person = Person({ 'name': 'testname' })
        assert person.original_attributes == {}
        person.save()
        assert person.original_attributes == {
            'name': 'testname',
            'id': person.id,
            'age': None
        }
        person.name = 'new'
        person.save()
        assert person.original_attributes == {
            'name': 'new',
            'id': person.id,
            'age': None
        }
