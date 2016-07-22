from request import Request
from errors import RecordNotFoundError
import util

class Scope:
    def __init__(self, model):
        self.model = model
        self.filter_clause = util.Hash()
        self.pagination_clause = util.Hash()
        self.order_clause = util.Hash()
        self.fields_clause = util.Hash()
        self.include_clause = util.Hash()

    def all(self):
        url = self.model.base_url()
        query_params = self.as_query_params()
        json = Request(self.model, params=query_params).get(url).json()
        return util.model_from_payload(json['data'], json)

    def where(self, clause):
        self.filter_clause.update(clause)
        return self

    def find(self, id):
        burl = self.model.base_url()
        path = "{base_url}/{id}".format(base_url=burl, id=id)
        query_params = self.as_query_params()
        response = Request(self.model, params=query_params).get(path)
        if response.status_code == 404:
            raise RecordNotFoundError(self.model, id)
        else:
            return util.model_from_payload(response.json()['data'], response.json())

    def first(self):
        return self.page(1).per(1).all()[0];

    def select(self, fields):
        namespace = self.model.jsonapi_type
        self.fields_clause[namespace] = fields
        return self

    def pluck(self, attribute):
        self.select([attribute])
        records = self.all()
        return map(lambda r: getattr(r, attribute), records)

    def includes(self, inclusions):
        directive = util.IncludeDirective(inclusions)
        util.deep_merge(self.include_clause, directive.to_dict())

        return self

    def per(self, size):
        self.pagination_clause['size'] = size
        return self

    def page(self, number):
        self.pagination_clause['number'] = number
        return self

    def order(self, order):
        if isinstance(order, dict):
            self.order_clause = order
        else:
            self.order_clause[order] = 'asc'
        return self

    def as_query_params(self):
        qp = {}
        if bool(self.filter_clause):
            qp.update(self.__filter_query_params())
        if bool(self.pagination_clause):
            qp.update(self.__pagination_query_params())
        if bool(self.order_clause):
            qp.update(self.__order_query_params())
        if bool(self.fields_clause):
            qp.update(self.__fields_query_params())
        if bool(self.include_clause):
            qp.update(self.__include_query_params())

        return qp

    # private

    def __filter_query_params(self):
        params = {}
        for key, value in self.filter_clause.iteritems():
            params['filter['+key+']'] = value
        return params

    def __include_query_params(self):
        directive = util.IncludeDirective(self.include_clause)
        return { 'include': directive.to_string() }

    def __fields_query_params(self):
        params = {}
        namespace, fields = self.fields_clause.items()[0]
        fields = ",".join(fields)
        return { 'fields[' + namespace + ']': fields }

    def __pagination_query_params(self):
        params = {}
        if 'number' in self.pagination_clause:
            params['page[number]'] = self.pagination_clause['number']
        if 'size' in self.pagination_clause:
            params['page[size]'] = self.pagination_clause['size']
        return params

    def __order_query_params(self):
        attribute, direction = self.order_clause.items()[0]
        if direction == 'desc':
            attribute = '-' + attribute
        return { 'sort': attribute }
