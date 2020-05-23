import enum

from pony import orm


class EnumConverter(orm.dbapiprovider.StrConverter):
    """Converter which can be used to store Enum values in the database."""
    def validate(self, val):
        if not isinstance(val, enum.Enum):
            raise ValueError('Must be an Enum.  Got {}'.format(type(val)))
        return val

    def py2sql(self, val):
        return val.name

    def sql2py(self, value):
        # Any enum type can be used, so py_type ensures the correct one is used to create the enum instance
        return self.py_type[value]


class SlottedEntityMixin:
    """Convnience mixin to update all related classes when updating this one."""
    def after_update(self):
        for attr in self._attrs_:
            print(attr)
