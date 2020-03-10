from pony import orm

from database.db import db
from database.constants import common


class AreaPOI(db.Entity):
    id = orm.PrimaryKey(int)
    importance = orm.Required(int)
    icon = orm.Required(int)
    faction_id = orm.Required(int)
    x = orm.Required(float)
    y = orm.Required(float)
    z = orm.Required(float)
    continent_id = orm.Required(int)
    flags = orm.Required(int, unsigned=True)
    area_id = orm.Required(int, unsigned=True)
    name = orm.Required(common.MultiString)
    description = orm.Optional(common.MultiString)
    world_state_id = orm.Required(int)
