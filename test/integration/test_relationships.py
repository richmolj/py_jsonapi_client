from mock import patch
from mock import MagicMock
import requests
from ..fixtures import *
from ..helpers import *
import py_jsonapi_client as japi

# NB - the tests asserting against a payload are run this
# way because the spec server does not implement this logic
# Once we extract various libaries, we can implement this
# behavior in the test server and adjust the tests

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
    # should only include the pet with dirty
    # toys in the request
    def test_saving_dirty_subrelations(self):
        expected_payload = {
            'data': {
                'id': '44',
                'type': 'people',
                'relationships': {
                    'pets': {
                        'data': [
                            {
                                'type': 'pets',
                                'id': '999',
                                'relationships': {
                                    'toys': {
                                        'data': [
                                            {
                                                'type': 'toys',
                                                'id': '34'
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

        person = Person({ 'id': '44' })
        toy = Toy({ 'id': '33' })
        toy.mark_persisted()
        pet1 = Pet({'id': '999', 'toys': [toy] })
        pet1.mark_persisted()
        pet2 = Pet({ 'id': '7', 'toys': [Toy()] })
        pet2.mark_persisted()
        person.pets = [pet1, pet2]
        person.mark_persisted()
        assert person.changed_relations(recursive=True) == {}
        new_toy = Toy({ 'id': '34' })
        new_toy.mark_persisted()
        person.pets[0].toys.append(new_toy)

        for mocked in self.mocked_request('put'):
            person.save({ 'relationships': [{ 'pets': 'toys' }, 'company'] })
            assert mocked.call_args[1]['json'] == expected_payload

    def test_saving_singular_marked_for_destruction(self):
        expected_payload = {
            'data': {
                'id': '44',
                'type': 'people',
                'relationships': {
                    'company': {
                        'data': {
                            'type': 'companies',
                            'id': '999',
                            'attributes': { '_destroy': True }
                        }
                    }
                }
            }
        }

        company = Company({ 'id': '999' })
        company.mark_persisted()
        person = Person({ 'id': '44', 'company': company })
        person.mark_persisted()
        person.company.mark_for_destruction()

        for mocked in self.mocked_request('put'):
            person.save({ 'relationships': 'company' })
            assert mocked.call_args[1]['json'] == expected_payload

    def test_saving_singular_marked_for_disassociation(self):
        expected_payload = {
            'data': {
                'id': '44',
                'type': 'people',
                'relationships': {
                    'company': {
                        'data': {
                            'type': 'companies',
                            'id': '999',
                            'attributes': { '_delete': True }
                        }
                    }
                }
            }
        }

        company = Company({ 'id': '999' })
        company.mark_persisted()
        person = Person({ 'id': '44', 'company': company })
        person.mark_persisted()
        person.company.mark_for_disassociation()

        for mocked in self.mocked_request('put'):
            person.save({ 'relationships': 'company' })
            assert mocked.call_args[1]['json'] == expected_payload

    def test_saving_plural_marked_for_destruction(self):
        expected_payload = {
            'data': {
                'id': '44',
                'type': 'people',
                'relationships': {
                    'pets': {
                        'data': [
                            {
                                'type': 'pets',
                                'id': '7',
                                'attributes': { '_destroy': True }
                            }
                        ]
                    }
                }
            }
        }

        pet1 = Pet({ 'id': '999' })
        pet1.mark_persisted()
        pet2 = Pet({ 'id': '7' })
        pet2.mark_persisted()
        person = Person({ 'id': '44', 'pets': [pet1, pet2] })
        person.mark_persisted()
        pet2.mark_for_destruction()

        for mocked in self.mocked_request('put'):
            person.save({ 'relationships': 'pets' })
            assert mocked.call_args[1]['json'] == expected_payload

    def test_saving_plural_marked_for_disassociation(self):
        expected_payload = {
            'data': {
                'id': '44',
                'type': 'people',
                'relationships': {
                    'pets': {
                        'data': [
                            {
                                'type': 'pets',
                                'id': '7',
                                'attributes': { '_delete': True }
                            }
                        ]
                    }
                }
            }
        }

        pet1 = Pet({ 'id': '999' })
        pet1.mark_persisted()
        pet2 = Pet({ 'id': '7' })
        pet2.mark_persisted()
        person = Person({ 'id': '44', 'pets': [pet1, pet2] })
        person.mark_persisted()
        pet2.mark_for_disassociation()

        for mocked in self.mocked_request('put'):
            person.save({ 'relationships': 'pets' })
            assert mocked.call_args[1]['json'] == expected_payload
