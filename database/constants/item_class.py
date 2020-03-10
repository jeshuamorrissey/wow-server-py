from pony import orm

from database.db import db
from database.constants import common


class ItemClass(db.Entity):
    id = orm.PrimaryKey(int)
    subclass_map = orm.Required(int)
    flags = orm.Required(int)
    name = orm.Required(common.MultiEnumString)
