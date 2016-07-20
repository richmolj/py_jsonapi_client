import inflection
from attribute import Attribute
import py_jsonapi_client as japi

class Base(Attribute):
    relation = True
    class_name = None

    def __init__(self, **options):
        if 'class_name' in options:
            self.class_name = options['class_name']

    def __set__(self, obj, value):
        value = self.__convert_assignment_payload_to_object(value)
        obj.relations[self.name] = value

    def __get__(self, obj, objtype):
        return obj.relations[self.name]

    def klass(self):
        klass_name = self.class_name or self.__inferred_class_name()
        if hasattr(klass_name, '__call__'):
            return klass_name()
        else:
            return japi._models[klass_name]

    # private

    def __inferred_class_name(self):
        class_name = inflection.singularize(self.name)
        class_name = inflection.titleize(class_name)
        class_name = class_name.replace(' ', '')
        return class_name

    def __convert_assignment_payload_to_object(self, payload):
        if isinstance(payload, dict):
            return self.klass()(payload)
        elif isinstance(payload, list):
            return map(lambda x: self.__convert_assignment_payload_to_object(x), payload)
        elif isinstance(payload, japi.Model):
            return payload
