from pony import orm

from database import constants, game
from database.db import db


class StartingItems(db.Entity):
    """StartingItems decides which items should be given to players on creation."""
    race = orm.Required(constants.EChrRaces)
    class_ = orm.Required(constants.EChrClasses)
    gender = orm.Required(game.Gender)
    orm.PrimaryKey(race, class_, gender)

    # The JSON here has the following structure:
    # {"entry": [int], "equipment_slot": [int]}
    equipment = orm.Required(orm.Json)

    # The JSON here is a list of entries.
    items = orm.Required(orm.Json)
