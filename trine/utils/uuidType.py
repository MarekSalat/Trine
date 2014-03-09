import uuid

from sqlalchemy import types
from sqlalchemy.dialects.mssql.base import MSBinary
from sqlalchemy.schema import Column


class UUID(types.TypeDecorator):
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
            return uuid.UUID(bytes=value)
        else:
            return None

    def is_mutable(self):
        return False


id_column_name = "id"


def id_column():
    import uuid

    return Column(UUID(), primary_key=True, default=uuid.uuid4)
