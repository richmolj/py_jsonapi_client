class Attribute(object):
    name      = None
    serialize = True

    def __init__(self, opts = {}):
        if 'name' in opts:
            self.name = opts['name']

    def __get__(self, obj, objtype):
        raw_value = obj.attributes[self.name]
        return raw_value

    def __set__(self, obj, value):
        obj.attributes[self.name] = value
