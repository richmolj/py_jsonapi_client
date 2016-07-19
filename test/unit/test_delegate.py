import py_jsonapi_client as japi

class PostHistoryNote(object):
    text = 'A note'

class PostHistory(object):
    revisions = [1,2,3]
    note      = PostHistoryNote()

    def revision_count(self):
        return 3

class Post(japi.Model):
    revisions      = japi.util.delegate(to='history')
    revision_count = japi.util.delegate(to='history')
    text           = japi.util.delegate(to='history.note')
    note_text      = japi.util.delegate(to='history.note', via='text')

    history        = PostHistory()

class TestDelegation(object):

    def test_class_level_delegation(self):
        assert Post.revisions == [1,2,3]

    def test_instance_level_delegation(self):
        post = Post()
        assert post.revisions == [1,2,3]

    def test_function_delegation(self):
        assert Post.revision_count() == 3

    def test_alternate_method_names(self):
        assert Post.note_text == 'A note'

    def test_multi_level_delegation(self):
        assert Post.text == 'A note'

    def test_set(self):
        post = Post()
        post.text = 'New note'
        assert post.text == 'New note'
        assert post.history.note.text == 'New note'

