import enum

from pony import orm

from typing import Tuple

from database.db import db


class AuraTemplate(db.Entity):
    id = orm.PrimaryKey(int, auto=True, min=10)

    name = orm.Optional(str)
    description = orm.Optional(str)
    strength_bonus = orm.Optional(int)

    instances = orm.Set('Aura')