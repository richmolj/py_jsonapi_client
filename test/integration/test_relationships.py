from mock import patch
from mock import MagicMock
import requests
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

    def mocked_request(self, verb):
        response = MagicMock()
        response.status_code = 201
        response.json = MagicMock(return_value={})
        with patch.object(requests, verb, return_value=response) as mocked:
            yield mocked

    def test_saving_with_relations(self):
        expected_create_payload = {
            'data': {
                'type': 'people',
                'attributes': {
                    'name': 'Pete',
                },
                'relationships': {
                    'company': {
                        'data': {
                            'type': 'companies',
                            'attributes': {
                                'name': 'Enron'
                            }
                        }
                    },
                    'pets': {
                        'data': [
                            {
                                'type': 'pets',
                                'attributes': { 'name': 'dog' },
                                'relationships': {
                                    'toys': {
                                        'data': [
                                            {
                                                'type': 'toys',
                                                'attributes': { 'name': 'frisbee' }
                                            }
                                        ]
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }

        person = Person({ 'name': 'Pete' })
        person.pets = [{ 'name': 'dog', 'toys': [{ 'name': 'frisbee' }] }]
        person.company = Company({ 'name': 'Enron' })

        for mocked in self.mocked_request('post'):
            person.save({ 'relationships': [{ 'pets': 'toys' }, 'company'] })
            assert mocked.call_args[1]['json'] == expected_create_payload

    def test_saving_does_not_include_clean_relations(self):
        expected_payload = {
            'data': {
                'id': '44',
                'type': 'people',
                'relationships': {
                    'company': {
                        'data': {
                            'type': 'companies',
                            'id': '999'
                        }
                    }
                }
            }
        }

        person = Person({ 'id': '44', 'name': 'Pete' })
        person.pets = [{ 'id': '22', 'name': 'dog', 'toys': [{ 'id': '4', 'name': 'frisbee' }] }]
        person.company = Company({ 'id': '8', 'name': 'Enron' })
        person.mark_persisted()
        for pet in person.pets:
            pet.mark_persisted()
            for toy in pet.toys:
                toy.mark_persisted()
        new_company = Company({ 'id': '999', 'name': 'trader joes' })
        new_company.mark_persisted()
        person.company = new_company

        for mocked in self.mocked_request('put'):
            person.save({ 'relationships': [{ 'pets': 'toys' }, 'company'] })
            assert mocked.call_args[1]['json'] == expected_payload

    # pets is not dirty, but pet toys are
    def test_saving_dirty_subrelations(self):
                expected_payload = {
            'data': {
                'id': '44',
                'type': 'people',
                'relationships': {
                    'company': {
                        'data': {
                            'type': 'companies',
                            'id': '999'
                        }
                    }
                }
            }
        }

