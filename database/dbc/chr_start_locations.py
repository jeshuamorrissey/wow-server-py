from pony import orm

from database.db import db
from database.dbc import constants as c


class ChrStartLocation(db.Entity):
    race = orm.PrimaryKey(c.Race)

    # Location information.
    map = orm.Required(int)
    zone = orm.Required(int)
    x = orm.Required(float)
    y = orm.Required(float)
    z = orm.Required(float)
    o = orm.Required(float)
