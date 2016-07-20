import util

class AttributeList(util.Hash):
    """
        Wrapper for list of defined attributes.

        foo = japi.Attribute()
        bar = japi.Attribute()

        This class now decorates the Hash of keys foo, bar
    """

    def relation_list(self):
        dct = {}
        for key, value in self.iteritems():
            if hasattr(value, 'relation'):
                dct[key] = value
        return dct
