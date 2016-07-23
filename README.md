py_jsonapi_client
=================

Python client for JSONAPI-compatible endpoints

### Basic Usage

```python
import py_jsonapi_client as japi

class ApplicationRecord(japi.Model):
    site = 'http://foo.com'
    namespace = 'api/v2'

class Person(japi.Model):
    name = japi.Attribute()

# GET http://foo.com/api/v2/people?page[number]=1&page[size]=1
person = Person.first()
person.name # => 'Joe'
```

### Testing

Tests use [nose2](http://nose2.readthedocs.io/).

* `python setup.py install`
* `python setup.py test`

(*Note: It is highly recommended to `pip install nose2` separately, to do
things like running a single test at a time*)

Integration tests hit a live JSONAPI-compatible server. This is the same
server [the ruby jsonapi_client](https://bbgithub.dev.bloomberg.com/InfrastructureExperience/jsonapi_client) uses. Start the server before running integration tests, or the tests will fail.

To start the Rails JSONAPI-compatible server:

* Clone https://bbgithub.dev.bloomberg.com/InfrastructureExperience/jsonapi_client
* Go to the dummy server: `cd jsonapi_client/spec/dummy`
* Install deps: `bundle install --binstubs`
* Create/Seed the DB: `bin/rake db:migrate && bin/rake db:seed`
* Run the server: `bin/rails s -p 3001`
* Run nose2 tests (within this project): `python setup.py test` or `nose2`
* Re-seed db if needed (within dummy rails app): `bin/rake
  db:migrate:reset && bin/rake db:seed`
