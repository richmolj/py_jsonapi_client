import py_jsonapi_client as japi

class ApplicationRecord(japi.Model):
    site = 'http://localhost:3001'
    namespace = 'api'

class Person(ApplicationRecord):
    path = '/people'

    name = japi.Attribute()
    age = japi.Attribute()

class Test(object):
    def setup(self):
        print 'setup'

    def teardown(self):
        print 'teardown'

class TestFinders(Test):
    def test_find(self):
        person = Person.find(1)
        assert person.name == 'John'

    def test_find_missing_record(self):
        raised = False
        try:
            Person.find(11111)
        except japi.RecordNotFoundError as e:
            raised = True
        assert raised == True

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

    def test_pagination(self):
        people = Person.per(2).page(2).all()
        assert len(people) == 2
        assert map(lambda p: p.name, people) == ['Bill', 'David']

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
        assert plucked_names == names

