from pony import orm

from database.db import db
from database.dbc import constants as c


class CharStartOutfit(db.Entity):
    race = orm.Required(c.Race)
    class_ = orm.Required(c.Class)
    gender = orm.Required(c.Gender)
    orm.PrimaryKey(race, class_, gender)

    # The JSON here has the following structure:
    # {"entry": [int], "equipment_slot": [int]}
    equipment = orm.Required(orm.Json)

    # The JSON here is a list of entries.
    items = orm.Required(orm.Json)
