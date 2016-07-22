class JsonApiError(Exception):
    def __init__(self, response):
        self.message = self.__error_message_from_jsonapi(response.json())

    def __str__(self):
        return self.message

    def __error_message_from_jsonapi(self, json):
        error = json['errors'][0]
        if 'detail' in error:
            return error['detail']
        else:
            return error['title']

class UndefinedAttributeError(Exception):
    def __init__(self, attr_name, obj):
        self.attr_name = attr_name
        self.obj = obj

    def __str__(self):
        return "Tried to assign '%s' to instance of %s. Forget to assign do.Attribute()?" % (self.attr_name, self.obj.__class__.__name__)

class RecordNotFoundError(Exception):
    def __init__(self, klass, record_id):
        self.klass = klass
        self.record_id = record_id

    def __str__(self):
        return "Failed to lookup %s with id %s" % (self.klass.__name__, self.record_id)

class LinkNotFoundError(Exception):
    def __init__(self, association_name):
        self.association_name = association_name

    def __str__(self):
        return "No links found for relation " + association_name

class UnauthenticatedError(JsonApiError):
    pass

class ServerError(JsonApiError):
    pass

class AccessDeniedError(JsonApiError):
    pass

class InvalidFieldError(JsonApiError):
    pass
