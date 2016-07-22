from ..fixtures import *
from ..helpers import *
from mock import patch

import py_jsonapi_client as japi

class TestDirtyTracking(object):

    def test_changed_attributes(self):
        post = Post({ 'body': 'postbody', 'title': 'posttitle' })
        assert post.changed_attributes() == {}
        post.mark_persisted()
        post.title = 'changed'
        assert post.changed_attributes() == { 'title': 'changed' }

    def test_mark_clean_removes_errors(self):
        post = Post()
        post.errors['name'] = 'err'
        post.mark_clean()
        assert post.errors == {}

    def test_mark_clean_resets_original_attributes(self):
        post = Post({ 'title': 'foo' })
        post.mark_persisted()
        post.name = 'bar'
        post.mark_clean()

        assert post.original_attributes == { 'title': 'foo' }
