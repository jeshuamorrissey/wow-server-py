from pony import orm

from database.constants import common
from database.db import db


class ItemSubClass(db.Entity):
    class_ = orm.Required('ItemClass', reverse='item_sub_class_backlink')
    sub_class = orm.Required(int)
    prerequisiteProficiency = orm.Required(int, unsigned=True)
    postrequisiteProficiency = orm.Required(int, unsigned=True)
    flags = orm.Required(int)
    displayFlags = orm.Required(int)
    weaponParrySeq = orm.Required(int)
    weaponReadySeq = orm.Required(int)
    weaponAttackSeq = orm.Required(int)
    WeaponSwingSize = orm.Required(int)
    displayName = orm.Required(common.MultiEnumString)
    verboseName = orm.Optional(common.MultiString)

    orm.PrimaryKey(sub_class, class_)
