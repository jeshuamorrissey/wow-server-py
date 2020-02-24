import enum

from pony import orm

from database.db import db


class Enchantment(db.Entity):
    id = orm.PrimaryKey(int, auto=True)

    # Reverse mappings.
    applied_to = orm.Optional('ItemEnchantment')
