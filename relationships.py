from request import Request
from errors import LinkNotFoundError
import util

class Relationships(object):

    def fetch(self, association_name, scope = None):
        links = self.links[association_name]
        relation = self.relation_list()[association_name]

        if links and 'related' in links:
            params = {}
            if scope:
                params = scope.as_query_params()
            response = Request(relation.klass(), params=params).link(links['related'])
            models = util.model_from_payload(response.json()['data'], response.json())
            setattr(self, association_name, models)
        else:
            raise LinkNotFoundError(association_name)
