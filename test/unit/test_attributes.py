from nose2.tools import *
from ..fixtures import *
from ..namespace_helper import NamespacedModel

import py_jsonapi_client as japi

class TestInstantiation(object):

    def test_empty_attributes(self):
        post = Post()
        assert post.attributes == {}

    def test_basic_attributes(self):
        post = Post({'title': 'Man Bites Dog'})
        assert post.title == 'Man Bites Dog'

    def test_undefined_attribute_dropped(self):
        post = Post({'asdf': 'something'})
        assert post.attributes == {}

class TestDirectAssignment(object):

    def test_blanks(self):
        post = Post()
        assert post.title == None

    def test_basic_assignment(self):
        post = Post()
        post.title = 'Man Bites Dog'
        assert post.title == 'Man Bites Dog'

class TestIntrospection(object):

    def test_attributes(self):
        post = Post({'title': 'Man Bites Dog'})
        assert post.attributes == {'title': 'Man Bites Dog'}

class TestSubclassing(object):

    def test_attributes_inherited(self):
        post = SpecialPost({'title': 'Man Bites Dog'})
        assert post.title == 'Man Bites Dog'

    def test_python_special_properties_not_inherited(self):
        assert SpecialPost.__module__ != NamespacedModel.__module__
        assert SpecialPost.__doc__ != Post.__doc__

    def test_properties_inherited(self):
        assert SpecialPost.basic == True
