import util

class IncludeDirective(object):
    def __init__(self, include_args):
        include_hash = self.parse_include_args(include_args)
        self.dct = {}
        for key, value in include_hash.iteritems():
            self.dct[key] = IncludeDirective(value)

    def to_dict(self):
        dct = {}
        for key, value in self.dct.iteritems():
            dct[key] = value.to_dict()
        return dct

    def parse_include_args(self, include_args):
        if isinstance(include_args, basestring):
            return { include_args: {} }
        elif isinstance(include_args, dict):
            return self.__parse_dict(include_args)
        elif isinstance(include_args, list):
            return self.__parse_list(include_args)
        else:
            return {}

    # private

    def __parse_dict(self, include_dict):
        parsed = {}
        for key, value in include_dict.iteritems():
            parsed[key] = self.parse_include_args(value)
        return parsed

    def __parse_list(self, include_list):
        parsed = {}
        for value in include_list:
            util.deep_merge(parsed, self.parse_include_args(value))
        return parsed
