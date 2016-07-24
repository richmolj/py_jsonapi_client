import uuid
from scope import Scope
from model_meta import ModelMeta
from errors import UndefinedAttributeError
from attribute import Attribute
from persistence import Persistence
from relationships import Relationships
import util

class Model(Relationships, Persistence):
    __metaclass__ = ModelMeta

    site = None
    namespace = None
    path = None
    relation_list = util.delegate(to='attribute_list')
    marked_for_destruction = False
    marked_for_disassociation = False

    find     = util.delegate(to='scope')
    where    = util.delegate(to='scope')
    order    = util.delegate(to='scope')
    all      = util.delegate(to='scope')
    first    = util.delegate(to='scope')
    per      = util.delegate(to='scope')
    page     = util.delegate(to='scope')
    select   = util.delegate(to='scope')
    pluck    = util.delegate(to='scope')
    includes = util.delegate(to='scope')

    id = Attribute()

    @classmethod
    def scope(self):
        return Scope(self)

    @classmethod
    def base_url(self):
        url = self.site
        if self.namespace:
            url += "/{namespace!s}".format(namespace=self.namespace)
        url += self.path
        return url

    def __init__(self, attributes = {}):
        self.uuid = uuid.uuid4()
        self.attributes = util.Hash()
        self.relations = util.Hash()
        self.errors = util.Hash()
        self.original_attributes = util.Hash()
        self.original_relations = util.Hash()
        self.links = util.Hash()

        for key, value in attributes.iteritems():
             self.__set_attribute(key, value)

    def __eq__(self, other):
        if other == None:
            return False
        else:
            return self.uuid == other.uuid

    def __repr__(self):
        """
            Rails-style string representation. Ex:
            #<models.Person@0x12a8db50 id: 123, name: "John Doe">
        """

        return util.friendly_repr(self)

    def assign_attributes(self, assignments):
        """
            Same as update_attributes without the save
            Ensures only valid attributes get set
        """
        for key, value in assignments.iteritems():
             self.__set_attribute(key, value)

    # Private

    def __set_attribute(self, key, value):
        if key in self.attribute_list:
            setattr(self, key, value)
