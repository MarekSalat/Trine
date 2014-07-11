from sprox.sa.provider import SAORMProvider
from sqlalchemy.orm import class_mapper, Mapper, Query
from sprox.sa.support import PropertyLoader, resolve_entity

__author__ = 'Marek'


class TrineProvider(SAORMProvider):
    pass

    def dictify(self, obj, fields=None, omit_fields=None):
        if obj is None:
            return {}
        r = {}
        mapper = class_mapper(obj.__class__)
        for prop in mapper.iterate_properties:
            if fields and prop.key not in fields:
                continue

            if omit_fields and prop.key in omit_fields:
                continue

            value = getattr(obj, prop.key)

            if value is None:
                continue

            if value is not None:
                if isinstance(prop, PropertyLoader):
                    klass = prop.argument
                    if isinstance(klass, Mapper):
                        klass = klass.class_
                    pk_name = self.get_primary_field(klass)
                    if isinstance(value, list) or isinstance(value, Query):
                        pass
                        # joins
                        value = [self.dictify(value, fields, omit_fields) for value in value]
                    else:
                        pass
                        # fks
                        value = self.dictify(value, fields, omit_fields)
            r[prop.key] = value
        return r