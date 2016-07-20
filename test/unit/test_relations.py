from ..fixtures import *
from ..helpers import *

import py_jsonapi_client as japi

class TestSetters(object):

    def test_instantiation_assignment(self):
        post = Post({'creator': {'name': 'Stephen King'}})
        assert isinstance(post.creator, Author)
        assert post.creator.name == 'Stephen King'

    def test_dict_assignment(self):
        post = Post()
        post.creator = {'name': 'Stephen King'}

        assert isinstance(post.creator, Author)
        assert post.creator.name == 'Stephen King'

    def test_object_assignment(self):
        post = Post()
        post.author = Author({'name': 'Stephen King'})

        assert isinstance(post.author, Author)
        assert post.author.name == 'Stephen King'

    def test_implicit_name(self):
        post = Post({ 'rating': { 'stars': 5 } })
        assert isinstance(post.rating, Rating) == True
        assert post.rating.stars == 5

    def test_list_dict_assignment(self):
        post = Post()
        post.comments = [{'text': 'Good'}, {'text': 'Bad'}]

        assert len(post.comments) == 2
        assert all(isinstance(c, Comment) for c in post.comments)
        assert map(lambda c: c.text, post.comments) == ['Good', 'Bad']

    def test_list_object_assignment(self):
        post = Post()
        post.comments = [Comment({'text': 'Good'}), Comment({'text': 'Bad'})]

        assert len(post.comments) == 2
        assert all(isinstance(c, Comment) for c in post.comments)
        assert map(lambda c: c.text, post.comments) == ['Good', 'Bad']

class TestIntrospection(object):

    def test_relation_list(self):
        assert matchArray(Post.relation_list().keys(), ['rating', 'comments', 'creator'])

    def test_klass(self):
        assert Post.relation_list()['comments'].klass() == Comment

class TestExplicitNamespace(object):

    def test_class_name(self):
        assert Introspector.relation_list()['explicit_namespace'].klass() == namespace_helper.NamespacedModel
