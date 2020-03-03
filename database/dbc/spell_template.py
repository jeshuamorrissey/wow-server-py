import enum

from pony import orm

from typing import Tuple

from database.db import db


class SpellTemplate(db.Entity):
    id = orm.PrimaryKey(int, auto=True, min=10)

    aura_instances = orm.Set('Aura')