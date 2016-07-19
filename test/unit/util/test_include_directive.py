from nose2.tools import *

import py_jsonapi_client as japi

class TestIncludeDirective(object):

    def test_array_of_strings_and_dicts(self):
        args = [
            'friends',
            { 'comments': ['author'] },
            { 'posts': ['author', { 'comments': ['author'] }] }
        ]
        directive = japi.util.IncludeDirective(args)
        dct = directive.to_dict()

        expected = {
            'friends': {},
            'comments': { 'author': {} },
            'posts': { 'author': {}, 'comments': { 'author': {} } }
        }

        assert expected == dct

    def test_simple_string(self):
        directive = japi.util.IncludeDirective('friends')
        dct = directive.to_dict()
        assert { 'friends': {} } == dct

    def test_simple_dict(self):
        directive = japi.util.IncludeDirective({ 'comments': 'author' })
        dct = directive.to_dict()
        assert { 'comments': { 'author': {} } } == dct

    def test_simple_list(self):
        directive = japi.util.IncludeDirective(['friends', 'comments'])
        dct = directive.to_dict()
        assert { 'friends': {}, 'comments': {} } == dct
