import copy
from request import Request
from validation import Validation
import util

class Persistence(object):

    persisted = False

    def mark_persisted(self):
        self.persisted = True
        self.mark_clean()

    def mark_clean(self):
        self.errors = {}

        if self.persisted:
            # must deep copy otherwise a normal set will affect this
            self.original_attributes = copy.deepcopy(self.attributes)
            self.original_relations = copy.deepcopy(self.relations)

    def changed_attributes(self):
        return util.changed_attributes(self)

    def changed_relations(self, **opts):
        return util.changed_relations(self, **opts)

    def save(self, opts = {}):
        relationships = {}
        if 'relationships' in opts:
            relationships = opts['relationships']
        response = self.__update_or_save(relationships)
        self.__after_save(response)
        return Validation(self).validate_response(response)

    def update_attributes(self, updates):
        self.assign_attributes(updates)
        return self.save()

    def destroy(self):
        request = Request(self)
        url = self.base_url() + '/' + self.id
        response = request.destroy(url)
        return Validation(self).validate_response(response)

    def reload(self):
        found = self.find(self.id)
        self.attributes = found.attributes
        self.mark_persisted()
        return self

    # private

    def __update_or_save(self, relationships):
        save_params = util.SaveParams(self).generate({ 'relationships': relationships })
        request = Request(self, params=save_params)
        url = self.base_url()

        if self.persisted:
            url += '/' + self.id
            response = request.update(url)
        else:
            response = request.create(url)
        return response

    def __after_save(self, response):
        if response.status_code == 201 or response.status_code == 200:
            if 'data' in response.json():
                util.model_from_payload(
                        response.json()['data'],
                        response.json(),
                        update=self
                        )

    def __save_params(self, relationships):
        return util.SaveParams(self).generate({ 'relationships': relationships })
