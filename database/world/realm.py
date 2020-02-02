import enum

from pony import orm

from database.db import db


class Realm(db.Entity):
    class Type(enum.IntEnum):
        PVE = 0
        PVP = 1
        RP = 6
        RPPVP = 8

    name = orm.PrimaryKey(str)
    hostport = orm.Required(str)
    type = orm.Required(Type, default=Type.PVE)

    # Characters in this realm.
    characters = orm.Set('Player')

    # Flags
    is_recommended = orm.Required(bool, default=False)
    for_new_players = orm.Required(bool, default=False)
    is_offline = orm.Required(bool, default=False)
    is_unavailable = orm.Required(bool, default=False)
