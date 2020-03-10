import enum

from pony import orm

from database.db import db


class Aura(db.Entity):
    applied_to = orm.Required('Unit')
    slot = orm.Required(int)

    base_spell = orm.Required('Spell')
    expiry_time = orm.Required(int)

    orm.PrimaryKey(applied_to, slot)
