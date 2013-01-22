import json
from sqlalchemy.types import TypeDecorator
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.ext.mutable import Mutable


# Stolen from http://docs.sqlalchemy.org/en/latest/orm/extensions/mutable.html
# Allows us to encode dictionaries as JSON transparently on the Session object.
class JSONEncodedDict(TypeDecorator):
    "Represents an immutable structure as a json-encoded string."

    impl = MEDIUMTEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            try:
                value = json.loads(value)
            except ValueError:
                value = {}
        return value


class MutationDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutationDict."

        if not isinstance(value, MutationDict):
            if isinstance(value, dict):
                return MutationDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()


MutationDict.associate_with(JSONEncodedDict)
