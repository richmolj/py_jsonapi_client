from relations import HasMany
import py_jsonapi_client as japi

def model_from_payload(payload_slice, payload, **opts):
    instance = __instance(payload_slice, **opts)
    if not instance:
        return
    __process_attributes(instance, payload_slice)
    __process_relationships(instance, payload_slice, payload)
    return instance

def __instance(payload_slice, **opts):
    if 'update' in opts:
        return opts['update']
    else:
        klass = __model_for(payload_slice['type'])
        if klass:
            return klass()

def __process_attributes(instance, payload_slice):
    instance.assign_attributes(payload_slice['attributes'])
    if 'id' in payload_slice:
        instance.id = payload_slice['id']
        instance.mark_persisted()

def __process_relationships(instance, payload_slice, payload):
      for relation_name, record in __relationships_for(payload_slice, payload):
        relation = instance.relation_list()[relation_name]
        if relation:
            if isinstance(relation, HasMany):
                # Ensure prior records are not blown away
                prior = getattr(instance, relation_name)
                prior.append(record)
                setattr(instance, relation_name, prior)
            else:
                setattr(instance, relation_name, record)

def __relationships_for(payload_slice, payload):
    if not 'relationships' in payload_slice:
        return
    for relation_name, relation_payload in payload_slice['relationships'].iteritems():
        for record in __process_relationship(relation_payload, payload):
            yield relation_name, record

def __process_relationship(payload_slice, payload):
    if 'data' in payload_slice:
        data = payload_slice['data']
        if isinstance(data, list):
            for datum in data:
                for record in __process_relationship({ 'data': datum }, payload):
                    yield record
        else:
            id = data['id']
            type = data['type']
            included = __select_included(payload, type, id)
            record = model_from_payload(included, payload)
            yield record

def __select_included(payload, type, id):
    filter_fn = lambda i: i['id'] == id and i['type'] == type
    return filter(filter_fn, payload['included'])[0]

def __model_for(jsonapi_type):
    filter_fn = lambda m: m.jsonapi_type == jsonapi_type
    return filter(filter_fn, japi._models.values())[0]
