import inflection
import util
import py_jsonapi_client as japi
from attribute import Attribute
from attribute_list import AttributeList

class ModelMeta(type):
    def __new__(cls, name, parents, dct):
        parent = parents[0]
        ModelMeta.__assemble_subclass_dictionary(dct, parent, name)
        ModelMeta.__process_delegates(dct)
        ModelMeta.__process_attributes(dct)

        klass = super(ModelMeta, cls).__new__(cls, name, parents, dct)
        japi._models[name] = klass
        return klass

    @staticmethod
    def __is_model(parent):
        # It's not japi.Model inheriting type
        # and it's not inheriting japi.Model
        # it must be subclassing a Model
        return parent.__class__ != type and parent.__name__ != 'Model'

    @staticmethod
    def __assemble_subclass_dictionary(dct, parent, name):
        if ModelMeta.__is_model(parent):
            ModelMeta.__merge_parent_dictionary(parent, dct)
        if not 'jsonapi_type' in dct:
            dct['jsonapi_type'] = inflection.underscore(inflection.pluralize(name))
        if not 'path' in dct:
            dct['path'] = '/' + dct['jsonapi_type']
        return dct

    @staticmethod
    def __merge_parent_dictionary(parent, dct):
        parent_dct = parent.__dict__.copy()
        del parent_dct['__module__']
        del parent_dct['__doc__']
        del parent_dct['jsonapi_type']
        del parent_dct['path']
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
