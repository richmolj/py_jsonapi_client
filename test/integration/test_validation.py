from ..fixtures import *
from ..helpers import *
import py_jsonapi_client as japi

class TestValidation(object):

    def test_server_validation_error(self):
        person = Person({ 'age': 4 })
        assert person.save() == False
        assert person.errors['name'] == "can't be blank"

    def test_no_validation_error(self):
        person = Person({ 'name': 'testname' })
        assert person.save() == True
        assert person.errors == {}

    def test_errors_removed(self):
        person = Person({ 'age': 4 })
        person.save()
        assert bool(person.errors)
        person.name = 'testname'
        person.save()
        assert not bool(person.errors)
