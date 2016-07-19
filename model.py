from scope import Scope
from model_meta import ModelMeta
from errors import UndefinedAttributeError
import util

class Model(object):
    __metaclass__ = ModelMeta

    site = None
    namespace = None
    path = None

    find   = util.delegate(to='scope')
    where  = util.delegate(to='scope')
    order  = util.delegate(to='scope')
    all    = util.delegate(to='scope')
    first  = util.delegate(to='scope')
    per    = util.delegate(to='scope')
    page   = util.delegate(to='scope')
    select = util.delegate(to='scope')
    pluck  = util.delegate(to='scope')

    @classmethod
    def scope(self):
        return Scope(self)

    def __init__(self, attributes = {}):
        self.attributes = util.Hash()

        for key, value in attributes.iteritems():
             self.__set_attribute(key, value)

    # Private

    def __set_attribute(self, key, value):
        if key in self.attribute_list:
            setattr(self, key, value)
