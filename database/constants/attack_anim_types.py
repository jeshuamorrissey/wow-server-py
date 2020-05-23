from pony import orm

from database.constants import common
from database.db import db


class AttackAnimTypes(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(common.SingleString)

    attack_anim_kits_backlink = orm.Set('AttackAnimKits', reverse='anim_type')
