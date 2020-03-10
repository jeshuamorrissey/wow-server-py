from pony import orm

from database import enums
from database.constants import common
from database.db import db


class ChrClasses(db.Entity):
    id = orm.PrimaryKey(int)
    player_class = orm.Required(bool)
    damage_bonus_stat = orm.Required(enums.Stat)
    display_power = orm.Required(enums.PowerType)
    pet_name_token = orm.Required(common.SingleString)
    name = orm.Required(common.MultiEnumString)
    filename = orm.Required(common.SingleString)
    spell_class_set = orm.Required(int)
    flags = orm.Required(int)

    unit_backlink = orm.Set('Unit')
