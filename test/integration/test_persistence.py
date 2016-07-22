from ..fixtures import *
from ..helpers import *
import py_jsonapi_client as japi

class TestPersistence(object):

    def test_basic_create(self):
        person = Person({ 'name': 'mytestname' })
        person.save()
        found = Person.find(person.id)
        assert found.name == 'mytestname'

    def test_basic_update(self):
        person = Person({ 'name': 'updateme' })
        person.save()
        found = Person.find(person.id)
        assert found.name == 'updateme'
        person.name = 'updated'
        person.save()
        found = Person.find(person.id)
        assert found.name == 'updated'

    def test_basic_update_attributes(self):
        person = Person({ 'name': 'testname', 'age': 30 })
        assert person.name == 'testname'
        assert person.age == 30
        assert person.update_attributes({ 'age': 77 }) == True
        assert person.name == 'testname'
        assert person.age == 77
        found = Person.find(person.id)
        assert found.name == 'testname'
        assert found.age == 77

    def test_update_only_sends_changeset(self):
        person = Person({ 'name': 'updateme', 'age': 30 })
        person.save()

        # some other process updates the age
        Person.find(person.id).update_attributes({ 'age': 77 })

        # save the original, only updating name
        person.name = 'updated'
        person.save()

        # should only update the name
        final = Person.find(person.id)
        assert final.name == 'updated'
        assert final.age == 77

    def test_found_record_marked_persisted(self):
        found = Person.find(1)
        assert found.persisted == True

    def test_marked_persisted(self):
        person = Person({ 'name': 'mytestname' })
        assert person.persisted == False
        person.save()
        assert person.persisted == True
