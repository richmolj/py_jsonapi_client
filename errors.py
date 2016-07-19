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
