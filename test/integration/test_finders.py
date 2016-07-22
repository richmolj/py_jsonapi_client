from ..fixtures import *
from ..helpers import *
import py_jsonapi_client as japi

class TestFinders(object):
    def test_find(self):
        person = Person.find(1)
        assert person.name == 'John'

    @raises(japi.RecordNotFoundError)
    def test_find_missing_record(self):
        Person.find(11111)

    def test_where(self):
        scope  = Person.where({ 'name': 'John' })
        scope  = scope.where({ 'age': 27 })
        people = scope.all()
        assert people[0].name == 'John'

    def test_where_overrides(self):
        scope  = Person.where({ 'name': 'John' })
        scope  = scope.where({ 'name': 'Joe' })
        people = scope.all()
        assert people[0].name == 'Joe'

    def test_all(self):
        people = Person.all()
        assert len(people) == 10
        assert isinstance(people[0], Person)

    def test_per(self):
        people = Person.per(2).all()
        assert len(people) == 2
        assert matchArray(map(lambda p: p.name, people), ['John', 'Joe'])

    def test_page(self):
        people = Person.page(2).all()
        assert len(people) == 10
        names = map(lambda p: p.name, people)
        assert 'John' not in names

    def test_full_pagination(self):
        people = Person.per(2).page(2).all()
        assert len(people) == 2
        assert matchArray(map(lambda p: p.name, people), ['Bill', 'David'])

    def test_first(self):
        person = Person.where({ 'name': 'Bill' }).first()
        assert person.name == 'Bill'

    def test_sort_defaults_asc(self):
        people = Person.order('name').all()
        names = map(lambda p: p.name, people)
        sorted_names = sorted(names, key=lambda n: n)
        assert names == sorted_names

    def test_sort_by_hash(self):
        people = Person.order({ 'name': 'desc' }).all()
        names = map(lambda p: p.name, people)
        sorted_names = sorted(names, key=lambda n: n, reverse=True)
        assert names == sorted_names

    def test_select(self):
        person = Person.select(['name']).find(1)
        assert person.name == 'John'
        assert person.age == None

    def test_pluck(self):
        plucked_names = Person.pluck('name')
        names = map(lambda p: p.name, Person.all())

        assert matchArray(plucked_names, names)

    def test_includes(self):
        person = Person.includes(['tags', { 'pets': 'toys' }]).first()
        tag_names = map(lambda t: t.name, person.tags)
        pet_names = map(lambda p: p.name, person.pets)
        pet1_toy_names = map(lambda t: t.name, person.pets[0].toys)
        pet2_toy_names = map(lambda t: t.name, person.pets[1].toys)
        assert matchArray(tag_names, ['smart', 'funny'])
        assert matchArray(pet_names, ['Lassie', 'Spot'])
        assert matchArray(pet1_toy_names, ['ball'])
        assert matchArray(pet2_toy_names, ['bone'])

    def test_not_included_not_loaded(self):
        person = Person.includes('tags').first()
        assert len(person.tags) == 2
        assert len(person.pets) == 0

    def test_reload(self):
        person = Person({ 'name': 'testname' })
        person.save()
        person.name = 'foo'
        assert person.name == 'foo'
        person.reload()
        assert person.name == 'testname'
