from pony import orm

from database.db import db


class Enchantment(db.Entity):
    id = orm.PrimaryKey(int, auto=True)

    # Reverse mappings.
    item_enchantment_backlink = orm.Optional('ItemEnchantment')
