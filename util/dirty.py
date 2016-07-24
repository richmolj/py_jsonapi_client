# This module is considered private to 'persistence'

def changed_attributes(model):
    changes = {}
    for key, value in model.attributes.iteritems():
        if not model.original_attributes[key] == value:
            changes[key] = value
    return changes

def changed_relations(model, **opts):
    changes = {}
    for key, value in model.relations.iteritems():
        original_record = model.original_relations[key]
        if isinstance(value, list):
            dirty = __dirty_has_many(value, original_record or [], **opts)
            if len(dirty) > 0:
                changes[key] = dirty
        else:
            dirty = __dirty_singular(value, original_record, **opts)
            if dirty:
                changes[key] = dirty
    return changes

def __dirty_singular(new, original, **opts):
    if original == None:
        return new
    elif not original.uuid == new.uuid:
        return new
    elif 'recursive' in opts and bool(new.changed_relations()):
        return new

def __dirty_has_many(records, original_records, **opts):
    dirty = []
    original_uuids = map(lambda r: r.uuid, original_records)
    for record in records:
        if not record.uuid in original_uuids:
            dirty.append(record)
        elif 'recursive' in opts and bool(record.changed_relations()):
            dirty.append(record)
    return dirty
