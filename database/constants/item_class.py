from pony import orm

from database.constants import common
from database.db import db


class ItemClass(db.Entity):
    id = orm.PrimaryKey(int)
    subclass_map = orm.Required(int)
    flags = orm.Required(int)
    name = orm.Required(common.MultiEnumString)

    item_sub_class_backlink = orm.Set('ItemSubClass', reverse='class_')
