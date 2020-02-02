import enum

from pony import orm

from database.db import db


class Guild(db.Entity):
    id = orm.PrimaryKey(int, auto=True)

    members = orm.Set('Player')
