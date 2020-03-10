from pony import orm

from database.db import db


class AttackAnimKits(db.Entity):
    id = orm.PrimaryKey(int)
    item_subclass_id = orm.Required(int)
    anim_type = orm.Required('AttackAnimTypes', reverse='attack_anim_kits_backlink')
    anim_frequency = orm.Required(int)
    which_hand = orm.Required(int)
