from ..fixtures import *
from ..helpers import *
from mock import patch

import py_jsonapi_client as japi

class TestDirtyTracking(object):

    def test_changed_attributes(self):
        post = Post({ 'body': 'postbody', 'title': 'posttitle' })
        assert post.changed_attributes() == { 'body': 'postbody', 'title': 'posttitle' }
        post.mark_persisted()
        post.title = 'changed'
        assert post.changed_attributes() == { 'title': 'changed' }

    def test_mark_clean_removes_errors(self):
        post = Post()
        post.errors['name'] = 'err'
        post.mark_clean()
        assert post.errors == {}

    def test_mark_clean_removes_destruction(self):
        post = Post()
        post.mark_for_destruction()
        assert post.marked_for_destruction == True
        post.mark_clean()
        assert post.marked_for_destruction == False

    def test_mark_clean_removes_disassociation(self):
        post = Post()
        post.mark_for_disassociation()
        assert post.marked_for_disassociation == True
        post.mark_clean()
        assert post.marked_for_disassociation == False

    def test_mark_clean_resets_original_attributes(self):
        post = Post({ 'title': 'foo' })
        post.mark_persisted()
        post.name = 'bar'
        post.mark_clean()

        assert post.original_attributes == { 'title': 'foo' }

    def test_changed_singular_relationships(self):
        post = Post()
        orig_creator = Author()
        post.creator = orig_creator
        post.rating = Rating() # does not change
        post.mark_persisted()
        new_creator = Author()
        post.creator = new_creator
        assert post.changed_relations() == {
            'creator': new_creator,
        }

    # should only be part of changed_relations() if
    # actual object changed, not properties
    def test_changed_relation_attributes(self):
        post = Post({ 'comments': [Comment()] })
        post.mark_persisted()
        post.comments[0].text = 'foo'
        assert post.changed_relations() == {}

    def test_appended_has_many_relationships(self):
        post = Post({ 'comments': [Comment()] })
        post.mark_persisted()
        new_comment = Comment()
        post.comments.append(new_comment)
        assert len(post.comments) == 2
        assert post.changed_relations() == {
            'comments': [new_comment]
        }

    def test_marked_for_destruction_has_many(self):
        comment = Comment()
        comment.mark_persisted()
        post = Post({ 'comments': [comment] })
        post.mark_persisted()
        assert post.changed_relations() == {}
        comment.mark_for_destruction()
        assert post.changed_relations() == { 'comments': [comment] }

    def test_marked_for_destruction_singular(self):
        post = Post({ 'creator': Author() })
        post.mark_persisted()
        assert post.changed_relations() == {}
        post.creator.mark_for_destruction()
        assert post.changed_relations() == { 'creator': post.creator }

    def test_marked_for_disassociation_has_many(self):
        comment = Comment()
        comment.mark_persisted()
        post = Post({ 'comments': [comment] })
        post.mark_persisted()
        assert post.changed_relations() == {}
        comment.mark_for_disassociation()
        assert post.changed_relations() == { 'comments': [comment] }

    def test_marked_for_disassociation_singular(self):
        post = Post({ 'creator': Author() })
        post.mark_persisted()
        assert post.changed_relations() == {}
        post.creator.mark_for_disassociation()
        assert post.changed_relations() == { 'creator': post.creator }

    def test_recursive_changed_relations_singular(self):
        post = Post()
        creator = Author()
        post.creator = creator
        post.mark_persisted()
        post.creator.mark_persisted()
        assert post.changed_relations(recursive=True) == {}
        state = State()
        post.creator.state = state
        assert post.changed_relations(recursive=True) == { 'creator': creator }
        assert post.creator.changed_relations() == { 'state': state }

    def test_recursive_changed_relations_has_many(self):
        post = Post()
        comment = Comment()
        comment.mark_persisted()
        post.comments = [comment]
        post.mark_persisted()
        assert post.changed_relations(recursive=True) == {}
        author = Author()
        comment.author = author
        assert post.changed_relations(recursive=True) == {
            'comments': [comment]
        }
        assert comment.changed_relations() == { 'author': author }


