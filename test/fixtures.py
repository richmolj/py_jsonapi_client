import namespace_helper

import py_jsonapi_client as japi

class Post(japi.Model):
    basic = True

    title = japi.Attribute()

    creator  = japi.BelongsTo(class_name='Author')
    comments = japi.HasMany()
    rating   = japi.HasOne()

class SpecialPost(Post):
    """
        Special Doc
    """
    jsonapi_type = 'important_posts'

class Comment(japi.Model):
    text = japi.Attribute()

class Author(japi.Model):
    name = japi.Attribute()

class Rating(japi.Model):
    stars = japi.Attribute()

class Introspector(japi.Model):
    explicit_namespace = japi.BelongsTo(class_name=(lambda: namespace_helper.NamespacedModel))

### Integration

class ApplicationRecord(japi.Model):
    site = 'http://localhost:3001'
    namespace = 'api'

class Person(ApplicationRecord):
    path = '/people'

    name = japi.Attribute()
    age = japi.Attribute()

    tags = japi.HasMany()
    pets = japi.HasMany()

class Tag(ApplicationRecord):
    name = japi.Attribute()

class Pet(ApplicationRecord):
    name = japi.Attribute()

    toys = japi.HasMany()

class Toy(ApplicationRecord):
    name = japi.Attribute()
