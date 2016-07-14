from scope import Scope

class Model:
    site = None
    namespace = None
    path = None

    @classmethod
    def find(self, id):
        return self.scope().find(id)

    @classmethod
    def scope(self):
        return Scope(self)

    # todo proper delegation
    @classmethod
    def where(self, clause):
        return self.scope().where(clause)

    def __init__(self, attributes = {}):
        for key, value in attributes.iteritems():
            setattr(self, key, value)
