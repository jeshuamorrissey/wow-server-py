import enum

from pony import orm

from database.db import db


class Profession(db.Entity):
    id = orm.PrimaryKey(int, auto=True, min=10)

    name = orm.Required(str)
    known_by = orm.Set('PlayerProfession')
