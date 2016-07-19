from request import Request
import util

class Scope:
    def __init__(self, model):
        self.model = model
        self.filter_clause = util.Hash()
        self.pagination_clause = util.Hash()

    def all(self):
        url = self.__base_url()
        query_params = self.as_query_params()
        json = Request(self).get(url, params=query_params)
        models = []
        for item in json['data']:
            models.append(self.model(item['attributes']))
        return models

    def where(self, clause):
        self.filter_clause.update(clause)
        return self

    def find(self, id):
        path = "{base_url}/{id}".format(base_url=self.__base_url(), id=id)
        json = Request(self).get(path)
        return self.model(json['data']['attributes'])

    def first(self):
        return self.page(1).per(1).all()[0];

    def per(self, number):
        self.pagination_clause['number'] = number
        return self;

    def page(self, number):
        self.pagination_clause['size'] = number
        return self;

    def as_query_params(self):
        qp = {}
        if bool(self.filter_clause):
            for key, value in self.filter_clause.iteritems():
                qp['filter['+key+']'] = value
        if bool(self.pagination_clause):
            qp['page[number]'] = self.pagination_clause['number']
            qp['page[size]'] = self.pagination_clause['size']

        return qp

    # private

    def __base_url(self):
        url = self.model.site
        if self.model.namespace:
            url += "/{namespace!s}".format(namespace=self.model.namespace)
        url += self.model.path
        return url
