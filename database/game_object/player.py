from pony import orm

from database.game_object import unit


class Player(unit.Unit):
    # General character information.
    account = orm.Required('Account')
    realm = orm.Required('Realm')
    name = orm.Required(str, unique=True)

    # Game-object specific information.
    skin_color = orm.Required(int)
    face = orm.Required(int)
    hair_style = orm.Required(int)
    hair_color = orm.Required(int)
    feature = orm.Required(int)
