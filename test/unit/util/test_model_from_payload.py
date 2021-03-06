from nose2.tools import *
from ...fixtures import *

import py_jsonapi_client as japi

class TestModelFromPayload(object):

    def test_basic(self):
        payload = {
            'data': {
                'type': 'posts',
                'id': 2,
                'attributes': {
                    'title': 'test post'
                }
            }
        }
        model = japi.util.model_from_payload(payload['data'], payload)
        assert isinstance(model, Post)
        assert model.title == 'test post'
        assert model.id == 2

    def test_persisted(self):
        payload = {
            'data': {
                'type': 'posts',
                'id': 2,
                'attributes': {
                    'title': 'test post'
                }
            }
        }
        model = japi.util.model_from_payload(payload['data'], payload)
        assert model.persisted == True

    def test_null_id(self):
        payload = {
            'data': {
                'type': 'posts',
                'attributes': { }
            }
        }
        model = japi.util.model_from_payload(payload['data'], payload)
        assert isinstance(model, Post)


    def test_custom_jsonapi_type(self):
        payload = {
            'data': {
                'type': 'important_posts',
                'attributes': { }
            }
        }
        model = japi.util.model_from_payload(payload['data'], payload)
        assert isinstance(model, SpecialPost)

    def test_includes(self):
        payload = {
            'data': {
                'type': 'posts',
                'attributes': { },
                'relationships': {
                    'creator': {
                        'data': {
                            'type': 'authors',
                            'id': '76'
                        }
                    },
                    'rating': {
                        'data': {
                            'type': 'ratings',
                            'id': '46'
                        }
                    },
                    'comments': {
                        'data': [
                            { 'type': 'comments', 'id': '47' },
                            { 'type': 'comments', 'id': '52' }
                        ]
                    }
                }
            },
            'included': [
                {
                    'type': 'comments',
                    'id': '47',
                    'attributes': { 'text': 'my first comment' }
                },
                {
                    'type': 'comments',
                    'id': '52',
                    'attributes': { 'text': 'my second comment' }
                },
                {
                    'type': 'authors',
                    'id': '76',
                    'attributes': { 'name': 'Stephen King' }
                },
                {
                    'type': 'ratings',
                    'id': '46',
                    'attributes': { 'stars': 5 }
                }
            ]
        }
        model = japi.util.model_from_payload(payload['data'], payload)
        assert isinstance(model, Post)
        assert all(isinstance(c, Comment) for c in model.comments)
        assert len(model.comments) == 2
        assert model.comments[0].id == '47'
        assert model.comments[0].text == 'my first comment'
        assert model.comments[1].id == '52'
        assert model.comments[1].text == 'my second comment'
        assert isinstance(model.creator, Author)
        assert model.creator.id == '76'
        assert model.creator.name == 'Stephen King'
        assert isinstance(model.rating, Rating)
        assert model.rating.id == '46'
        assert model.rating.stars == 5

    def test_links(self):
        payload = {
            'data': {
                'id': '1',
                'type': 'posts',
                'attributes': { },
                'relationships': {
                    'comments': {
                        'links': {
                            'self': 'http://foo.com/api/posts/1/relationships/comments',
                            'related': 'http://foo.com/api/posts/1/comments'
                        }
                    }
                }
            }
        }
        model = japi.util.model_from_payload(payload['data'], payload)
        assert model.links == {
            'comments': {
                'self': 'http://foo.com/api/posts/1/relationships/comments',
                'related': 'http://foo.com/api/posts/1/comments'
            }
        }
