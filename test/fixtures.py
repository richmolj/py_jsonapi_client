import os
import namespace_helper

import py_jsonapi_client as japi

class Post(japi.Model):
    site = 'http://test.com'

    basic = True

    title = japi.Attribute()
    body = japi.Attribute()

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
    name = japi.Attribute()
    age = japi.Attribute()

    company = japi.BelongsTo()
    tags = japi.HasMany()
    pets = japi.HasMany()

class Company(ApplicationRecord):
    name = japi.Attribute()

class Tag(ApplicationRecord):
    name = japi.Attribute()

class Pet(ApplicationRecord):
    name = japi.Attribute()

    toys = japi.HasMany()

class Toy(ApplicationRecord):
    name = japi.Attribute()

class Admin(ApplicationRecord):
    name = japi.Attribute()

class AuthdAdmin(Admin):
    path = '/admins'
    jsonapi_type = 'admins'

    auth_header = 'Token token="{token!s}"'.format(token='4utht0k3n')

class ResponseCode(ApplicationRecord):
    code = japi.Attribute()
