import enum

from pony import orm

from database.db import db


class Aura(db.Entity):
    id = orm.PrimaryKey(int, auto=True, min=10)

    base_aura = orm.Required('AuraTemplate')
    duration_remaining = orm.Optional(int)
    applied_to = orm.Required('Unit')
