from ..fixtures import *
from ..helpers import *
from mock import patch

import py_jsonapi_client as japi

class PostResponse(object):
    status_code = 200

    def json(self):
        return {
           'data': {
                'id': 1,
                'type': 'posts',
                'attributes': {}
            }
        }


class TestPersistence(object):

    def test_not_persisted_when_new_record(self):
        post = Post({ 'id': 1 })
        assert post.persisted == False

    def test_mark_persisted(self):
        post = Post()
        assert post.persisted == False
        post.mark_persisted()
        assert post.persisted == True
