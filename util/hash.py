# Works more like a ruby Hash
#
# foo = {}
# foo['bar'] #=> None, instead of raising error

class Hash(dict):
    def __getitem__(self, key):
        if key in self:
            return self.get(key)
