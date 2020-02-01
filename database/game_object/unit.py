from pony import orm

from database.game_object.game_object import GameObject
from dbc import constants as c


class Unit(GameObject):
    level = orm.Required(int, min=1)
    race = orm.Required(c.Race)
    class_ = orm.Required(c.Class)
    gender = orm.Required(c.Gender)
