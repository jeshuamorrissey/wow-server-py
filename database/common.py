from pony import orm
import enum


class EnumConverter(orm.dbapiprovider.StrConverter):
    def validate(self, val):
        if not isinstance(val, enum.Enum):
            raise ValueError('Must be an Enum.  Got {}'.format(type(val)))
        return val

    def py2sql(self, val):
        return val.name

    def sql2py(self, value):
        # Any enum type can be used, so py_type ensures the correct one is used to create the enum instance
        return self.py_type[value]