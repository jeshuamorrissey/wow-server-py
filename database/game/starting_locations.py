from pony import orm

from database import enums
from database.db import db


class StartingLocations(db.Entity):
    """StartingLocations decides where players should start on the map."""
    race = orm.PrimaryKey(enums.EChrRaces)

    # Location information.
    map = orm.Required(int)
    zone = orm.Required(int)
    x = orm.Required(float)
    y = orm.Required(float)
    z = orm.Required(float)
    o = orm.Required(float)
