from pony import orm

from database.db import db
from database.constants import common


class Resistances(db.Entity):
    id = orm.PrimaryKey(int)
    flags = orm.Required(int)
    fizzle_sound_id = orm.Required(int)
    name = orm.Required(common.MultiEnumString)
