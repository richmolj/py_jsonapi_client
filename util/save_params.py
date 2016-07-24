import util

class SaveParams(object):
    def __init__(self, model):
        self.model = model

    def generate(self, opts = {}):
        params = self.__base_params()
        self.__presence_assign(params['data'], 'attributes', self.__attribute_params())

        if 'relationships' in opts:
            relation_params = self.__relation_params(opts['relationships'])
            self.__presence_assign(params['data'], 'relationships', relation_params)

        return params

    # private

    def __presence_assign(self, hash, key, value):
        if bool(value):
            hash[key] = value

    def __base_params(self):
        params = { 'data': { 'type': self.model.jsonapi_type } }
        if self.model.id != None:
            params['data']['id'] = self.model.id
        return params

    def __attribute_params(self):
        params = self.model.changed_attributes()
        params = util.dict_except(params, 'id')
        params.update(self.__destruction_params())
        return params

    def __destruction_params(self):
        params = {}
        # if self.model.marked_for_destruction:
            # params['_destroy'] = True
        # elif self.model.marked_for_disassociation:
            # params['_delete'] = True
        return params

    def __relation_params(self, relationships):
        params = {}
        for relation_name, records, nested in self.__iterate_relationships(relationships):
            relation_params = {}
            if isinstance(records, list):
                relation_params = self.__has_many_relation_params(records, nested)
            else:
                relation_params = self.__singular_relation_param(records, nested)

            params[relation_name] = relation_params
        return params

    def __iterate_relationships(self, relationships):
        directive = util.IncludeDirective(relationships)
        changed_relations = self.model.changed_relations(recursive=True)
        for relation_name, nested in directive.to_dict().iteritems():
            if relation_name in changed_relations:
                relations = getattr(self.model, relation_name)

                if isinstance(relations, list):
                    dirty = self.__has_many_dirty_records(relation_name, relations, changed_relations)
                    yield relation_name, dirty, nested
                else:
                    yield relation_name, relations, nested

    def __has_many_dirty_records(self, relation_name, records, changed_relations):
        dirty = []
        for record in records:
            if record in changed_relations[relation_name]:
                dirty.append(record)
        return dirty

    def __has_many_relation_params(self, records, nested):
        payloads = []
        for record in records:
            params = SaveParams(record).generate({ 'relationships': nested })
            payloads.append(params['data'])
        return { 'data': payloads }

    def __singular_relation_param(self, record, nested):
      return SaveParams(record).generate({ 'relationships': nested })
