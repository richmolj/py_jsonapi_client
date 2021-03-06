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

    def test_id_assignable(self):
        post = Post({ 'id': 1 })
        assert post.id == 1

class TestDirectAssignment(object):

    def test_blanks(self):
        post = Post()
        assert post.title == None

    def test_basic_assignment(self):
        post = Post()
        post.title = 'Man Bites Dog'
        assert post.title == 'Man Bites Dog'
        assert post.attributes == { 'title': 'Man Bites Dog' }

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
        assert SpecialPost.path != Post.path
        assert SpecialPost.jsonapi_type != Post.jsonapi_type

    def test_properties_inherited(self):
        assert SpecialPost.basic == True

class TestDerivations(object):

    def test_path_derived(self):
        assert Post.path == '/posts'

    def test_jsonapi_type_derived(self):
        assert Post.jsonapi_type == 'posts'

class TestRelations(object):

    def test_attributes_does_not_include_relations(self):
        post = Post({ 'title': 'mytitle', 'author': { 'name': 'Joe' } })
        assert 'author' not in post.attributes.keys()
