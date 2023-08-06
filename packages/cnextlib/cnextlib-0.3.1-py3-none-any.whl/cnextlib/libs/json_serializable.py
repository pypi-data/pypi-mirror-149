import simplejson as json

class JsonSerializable:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, ignore_nan=True)

    def __repr__(self) -> str:
        return self.toJSON()