from pony import orm

from database.constants import common
from database.db import db


class Resistances(db.Entity):
    id = orm.PrimaryKey(int)
    flags = orm.Required(int)
    fizzle_sound_id = orm.Required(int)
    name = orm.Required(common.MultiEnumString)
