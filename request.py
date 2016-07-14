import requests

class Request:
    def __init__(self, model):
        self.model = model

    def get(self, url, **opts):
        params = {}
        if 'params' in opts:
            params = opts['params']
        response = requests.get(url, params=params)
        return response.json()
