from colorize import colorize

def friendly_repr(model):
    """
        Rails-style string representation. Ex:
        #<models.Person@0x12a8db50 id: 123, name: "John Doe">
    """

    attrs = __friendly_attrs(model.attributes)
    model = model.__module__ + "." + model.__class__.__name__ + '@' + hex(id(model))
    return "#<%s %s>" % (colorize('yellow', model), colorize('bold', ", ".join(attrs)))

def __friendly_attrs(attributes):
    attrs = []
    for key, val in attributes.iteritems():
        if isinstance(val, basestring):
            val = '"%s"' % val
        attrs.append("%s: %s" % (key, val))
    return attrs
