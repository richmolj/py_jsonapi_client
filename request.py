import urllib
import pprint
import json
import requests
import util
from logger import logger
from errors import *

def error_handling(f):
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        if response.status_code == 401:
            raise UnauthenticatedError(response)
        if response.status_code == 400:
            raise InvalidFieldError(response)
        if response.status_code == 403:
            raise AccessDeniedError(response)
        elif response.status_code >= 500:
            raise ServerError(response)
        else:
            return response

    return wrapper

class Request:
    def __init__(self, model, **opts):
        self.model = model
        self.params = {}
        if 'params' in opts:
            self.params = opts['params']

    @error_handling
    def get(self, url):
        response = self.__req('get', url, self.params)
        return response

    @error_handling
    def update(self, url):
        response = self.__req('put', url, self.params)
        return response

    @error_handling
    def create(self, url):
        response = self.__req('post', url, self.params)
        return response

    @error_handling
    def destroy(self, url):
        response = self.__req('delete', url)
        return response

    # private

    def __req(self, verb, url, params = {}):
        func = getattr(requests, verb)
        headers = self.__derive_headers(self.model)
        self.__log_request(url, verb, params)

        response = None
        if verb == 'get':
            response = func(url, params=params, headers=headers)
        else:
            response = func(url, json=params, headers=headers)
        self.__log_response(response)
        return response

    def __log_response(self, response):
        status_code = response.status_code
        if status_code == 200 or status_code == 201 or status_code == 204:
            status_code = util.colorize('green', str(status_code))
        elif status_code == 422:
            status_code = util.colorize('yellow', str(status_code))
        elif status_code >= 500:
            status_code = util.colorize('red', str(status_code))
        else:
            status_code = util.colorize('bold', str(status_code))

        logger.debug(util.colorize('bold', 'Server Response: ') + util.colorize('bold', status_code))

        if response.status_code != 204: # delete may have no json
            logger.debug(json.dumps(response.json(), indent=2))

    def __log_request(self, url, verb, params):
        full_url = url
        if bool(params):
            if verb == 'get':
                full_url += '?' + urllib.urlencode(params)
        full_url = util.colorize('cyan', full_url)
        verb = util.colorize('magenta', verb.upper())
        logger.debug(verb + ' ' + full_url)

        if bool(params) and verb != 'get':
            logger.debug(json.dumps(params, indent=2))

    def __derive_headers(self, model):
        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json'
        }
        if hasattr(model, 'auth_header'):
            headers.update({ 'Authorization': self.model.auth_header })
        return headers
