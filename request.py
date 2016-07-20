import requests
from errors import *

def error_handling(f):
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        if response.status_code == 401:
            raise UnauthenticatedError
        if response.status_code == 403:
            raise AccessDeniedError
        elif response.status_code >= 500:
            raise ServerError
        else:
            return response

    return wrapper

class Request:
    def __init__(self, model):
        self.model = model

    @error_handling
    def get(self, url, **opts):
        params = {}
        if 'params' in opts:
            params = opts['params']
        response = self.__req('get', url, params)
        return response

    # private

    def __req(self, verb, url, params):
        func = getattr(requests, verb)

        headers = self.__derive_headers(self.model)
        return func(url, params=params, headers=headers)

    def __derive_headers(self, model):
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
        }
        if hasattr(model, 'auth_header'):
            headers.update({ 'Authorization': self.model.auth_header })
        return headers
