from pony import orm

from database.db import db
from database.constants import common


class ChrClasses(db.Entity):
    id = orm.PrimaryKey(int)
    player_class = orm.Required(int)
    damage_bonus_stat = orm.Required(int)
    display_power = orm.Required(int)
    pet_name_token = orm.Required(common.SingleString)
    name = orm.Required(common.MultiEnumString)
    filename = orm.Required(common.SingleString)
    spell_class_set = orm.Required(int)
    flags = orm.Required(int)
