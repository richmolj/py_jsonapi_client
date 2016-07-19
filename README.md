py_jsonapi_client
=================

Python client for JSONAPI-compatible endpoints

### Testing

* `python setup.py test`

Start the Rails JSONAPI-compatible server:

* Clone https://bbgithub.dev.bloomberg.com/InfrastructureExperience/jsonapi_client
* Go to the dummy server: `cd jsonapi_client/spec/dummy`
* Install deps: `bundle install --binstubs`
* Create/Seed the DB: `bin/rake db:migrate && bin/rake db:seed`
* Run the server: `bin/rails s -p 3001`
* Run nose2 tests (within this project): `nose2`
* Re-seed db if needed (within dummy rails app): `bin/rake
  db:migrate:reset && bin/rake db:seed`
