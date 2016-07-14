from nose.tools import *
from mock import patch
from mock import PropertyMock

import py_jsonapi_client as japi

class ApplicationRecord(japi.Model):
    site = 'http://localhost:3001'
    namespace = 'api'

class Person(ApplicationRecord):
    path = '/people'

class Test(object):
    def setup(self):
        print 'setup'

    def teardown(self):
        print 'teardown'

class TestFinders(Test):
    def test_find(self):
        person = Person.find(1)
        assert person.name == 'John'

    def test_where(self):
        scope  = Person.where({ 'name': 'John' })
        scope  = scope.where({ 'age': 27 })
        people = scope.all()
        assert people[0].name == 'John'

    def test_where_overrides(self):
        scope  = Person.where({ 'name': 'John' })
        scope  = scope.where({ 'name': 'Joe' })
        people = scope.all()
        assert people[0].name == 'Joe'

