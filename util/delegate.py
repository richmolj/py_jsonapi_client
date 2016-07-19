# https://docs.python.org/2/howto/descriptor.html
#
# N.B. set/delete operations only work with instances

import operator
from hash import Hash

class delegate(object):
    def __init__(self, **options):
        options        = Hash(options)
        self.to        = options['to']
        self.via       = options['via']
        self.allow_nil = options['allow_nil']

    def __get__(self, instance, cls):
        owner        = instance if instance else cls

        delegate_obj = operator.attrgetter(self.to)(owner)

        # Don't blow up if we allow nils
        if self.allow_nil:
            if not delegate_obj:
                return

        # If it's a function, call it
        if hasattr(delegate_obj, '__call__'):
            delegate_obj = delegate_obj()

        result  = getattr(delegate_obj, (self.via or self.name))

        return result

    def __set__(self, instance, value):
        delegate_obj = operator.attrgetter(self.to)(instance)
        setattr(delegate_obj, (self.via or self.name), value)
