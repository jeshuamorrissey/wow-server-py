from pony import orm

from database import constants
from database.db import db


class StartingStats(db.Entity):
    """StartingStats decides what player's starting stats should be."""
    race = orm.Required(constants.ChrRaces)
    class_ = orm.Required(constants.ChrClasses)

    # Location information.
    strength = orm.Required(int)
    agility = orm.Required(int)
    stamina = orm.Required(int)
    intellect = orm.Required(int)
    spirit = orm.Required(int)
    base_health = orm.Required(int)
    base_power = orm.Required(int)

    orm.PrimaryKey(race, class_)
