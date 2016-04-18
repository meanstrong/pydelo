from datetime import datetime
from flask.json import JSONEncoder as BaseJSONEncoder


class JSONEncoder(BaseJSONEncoder):
    def default(self, obj):
        if isinstance(obj, JsonSerializer):
            return obj.to_json()
        return super(JSONEncoder, self).default(obj)


class JsonSerializer(object):
    __json_hidden__ = None

    def to_json(self):
        hidden = self.__json_hidden__ or []
        value = dict()
        for p in self.__mapper__.iterate_properties:
            if isinstance(getattr(self, p.key), datetime):
                value[p.key] = str(getattr(self, p.key))
            else:
                value[p.key] = getattr(self, p.key)
        for key in hidden:
            value.pop(key, None)
        return value
