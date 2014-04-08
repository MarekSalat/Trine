import uuid

from sqlalchemy import types
from sqlalchemy.dialects.mssql.base import MSBinary
from sqlalchemy.schema import Column


class UuidColumn(types.TypeDecorator):
    impl = MSBinary

    def __init__(self):
        self.impl.length = 16
        types.TypeDecorator.__init__(self, length=self.impl.length)

    def process_bind_param(self, value, dialect=None):
        if value and isinstance(value, uuid.UUID):
            return value.bytes
        if value and isinstance(value, str):
            value = value.replace("-", "")
            return value.encode("UTF-8")
        elif value and not isinstance(value, uuid.UUID):
            raise ValueError('value %s %s is not a valid uuid.UUID' % value, type(value))
        else:
            return None

    def process_result_value(self, value, dialect=None):
        if value:
            return JsonableUUID(bytes=value)
        else:
            return None

    def is_mutable(self):
        return False

class JsonableUUID(uuid.UUID):

    def __json__(self):
        return str(self)

id_column_name = "id"


def id_column():
    import uuid

    return Column(UuidColumn(), primary_key=True, default=lambda : JsonableUUID(uuid.uuid4().hex))
