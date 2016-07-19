import util
from attribute import Attribute
from attribute_list import AttributeList

class ModelMeta(type):
    def __new__(cls, name, parents, dct):
        parent = parents[0]
        if ModelMeta.__is_model(parent):
            ModelMeta.__merge_parent_dictionary(parent, dct)

        ModelMeta.__process_delegates(dct)
        ModelMeta.__process_attributes(dct)

        klass = super(ModelMeta, cls).__new__(cls, name, parents, dct)
        return klass

    @staticmethod
    def __is_model(parent):
        # It's not japi.Model inheriting type
        # and it's not inheriting japi.Model
        # it must be subclassing a Model
        return parent.__class__ != type and parent.__name__ != 'Model'

    @staticmethod
    def __merge_parent_dictionary(parent, dct):
        parent_dct = parent.__dict__.copy()
        del parent_dct['__module__']
        del parent_dct['__doc__']
        dct.update(parent_dct)

    @staticmethod
    def __process_delegates(dct):
        for key, value in dct.iteritems():
            if isinstance(value, util.delegate):
                value.name = key

    @staticmethod
    def __process_attributes(dct):
        dct['attribute_list'] = AttributeList()

        for key, value in dct.iteritems():
            if isinstance(value, Attribute):
                dct['attribute_list'][key] = value
                value.name = key
