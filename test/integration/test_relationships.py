from ..fixtures import *
from ..helpers import *
import py_jsonapi_client as japi

class TestRelationships(object):
    def test_fetch_via_link(self):
        person = Person.first()
        assert len(person.pets) == 0
        person.fetch('pets')
        assert len(person.pets) == 2
        pet_names = map(lambda p: p.name, person.pets)
        assert matchArray(pet_names, ['Lassie', 'Spot'])

    def test_fetch_with_scope(self):
        person = Person.first()
        person.fetch('pets', Pet.per(1))
        assert len(person.pets) == 1
        assert person.pets[0].name == 'Spot'

    def test_fetch_merges_link_params(self):
        person = Person()
        person.links = {
            'pets': {
                'related': 'http://localhost:3001/api/pets?filter[person_id]=2'
            }
        }
        person.fetch('pets', Pet.where({ 'name': 'Elmo' }))
        assert len(person.pets) == 1
        assert person.pets[0].name == 'Elmo'

        person.fetch('pets', Pet.where({ 'name': 'Garfield' }))
        assert len(person.pets) == 1
        assert person.pets[0].name == 'Garfield'
