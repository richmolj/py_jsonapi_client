from scope import Scope
from model_meta import ModelMeta

class Model(object):
    __metaclass__ = ModelMeta

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

    # todo proper delegation
    @classmethod
    def all(self):
        return self.scope().all()

    def __init__(self, attributes = {}):
        for key, value in attributes.iteritems():
            setattr(self, key, value)
