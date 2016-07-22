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
            self.original_attributes = copy.deepcopy(self.attributes)
        else:
            self.original_attributes = {}

    def changed_attributes(self):
        changes = {}
        if bool(self.original_attributes):
            for key, value in self.attributes.iteritems():
                if not self.original_attributes[key] == value:
                    changes[key] = value
        return changes

    def save(self):
        response = self.__update_or_save()
        self.__after_save(response)
        return Validation(self).validate_response(response)

    def update_attributes(self, updates):
        self.assign_attributes(updates)
        return self.save()

    # private

    def __update_or_save(self):
        request = Request(self, params=self.__save_params())
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

    def __save_params(self):
        params = {
            'data': {
                'id': self.id,
                'type': self.jsonapi_type,
                'attributes': util.dict_except(self.attributes, 'id')
            }
        }

        if self.persisted:
            params['data']['attributes'] = self.changed_attributes()

        return params
