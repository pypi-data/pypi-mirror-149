
class DictOnes(dict):
    def __init__(self, keys=None, *values):
        if keys is None:
            return
        index = 0
        for key in [i.strip() for i in keys.split(',')]:
            if len(values) and len(values) >= index + 1:
                value = values[index]
            else:
                value = None
            self[key] = value
            index += 1
            
    def __getattr__(self, attrname):
        if attrname not in self:
            raise KeyError(attrname)
        return self[attrname]

    def __setattr__(self, attrname, value):
        self[attrname] = value

    def __delattr__(self, attrname):
        del self[attrname]

    def copy(self):
        return DictOnes(super(DictOnes, self).copy())