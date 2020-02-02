from pony import orm

from database.dbc import constants as c
from database.world.game_object.game_object import GameObject


class Unit(GameObject):
    level = orm.Required(int, min=1)
    race = orm.Required(c.Race)
    class_ = orm.Required(c.Class)
    gender = orm.Required(c.Gender)

    # For NPC units, they will link to a template.
    base_unit = orm.Optional('UnitTemplate')

    # For pets, they will have a master.
    master = orm.Optional('Player')

    # Unit location information.
    x = orm.Required(float)
    y = orm.Required(float)
    z = orm.Required(float)
    o = orm.Required(float)
