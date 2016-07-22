class Validation(object):
    def __init__(self, model):
        self.model = model

    def validate_response(self, response):
        if response.status_code == 422:
            for attribute, message in self.__response_errors(response.json()):
                self.model.errors[attribute] = message
            return False
        else:
            return True

    # private

    def __response_errors(self, response):
        for error in response['errors']:
            attribute = self.__extract_attribute(error)
            yield attribute, error['title']

    def __extract_attribute(self, error):
        return error['source']['pointer'].split('/')[-1]
