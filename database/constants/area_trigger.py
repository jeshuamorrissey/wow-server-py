from pony import orm

from database.db import db


class AreaTrigger(db.Entity):
    id = orm.PrimaryKey(int)
    continent_id = orm.Required(int)
    x = orm.Required(float)
    y = orm.Required(float)
    z = orm.Required(float)
    radius = orm.Required(float)
    box_length = orm.Required(float)
    box_width = orm.Required(float)
    box_height = orm.Required(float)
    box_yaw = orm.Required(float)
