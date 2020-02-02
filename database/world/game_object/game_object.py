from pony import orm

from database.db import db


class GameObject(db.Entity):
    id = orm.PrimaryKey(int, auto=True, min=1)
    entry = orm.Optional(int)
    scale = orm.Required(float, default=1.0)
