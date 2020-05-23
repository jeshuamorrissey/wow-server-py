from pony import orm

from database.db import db


class Aura(db.Entity):
    applied_to = orm.Required('Unit', reverse='auras')
    applied_by = orm.Required('Unit', reverse='applied_auras')
    slot = orm.Required(int)

    base_spell = orm.Required('Spell')
    expiry_time = orm.Required(int)
    applications = orm.Required(int, default=1)

    orm.PrimaryKey(applied_to, slot)
