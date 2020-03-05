import enum

from pony import orm

from database.db import db


class GuildMembership(db.Entity):
    player = orm.PrimaryKey('Player')
    guild = orm.Required('Guild')
    rank = orm.Required(int)


class Guild(db.Entity):
    id = orm.PrimaryKey(int, auto=True, min=10)

    members = orm.Set('GuildMembership')
