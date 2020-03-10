from pony import orm

from database.db import db


class BankBagSlotPrices(db.Entity):
    id = orm.PrimaryKey(int)
    cost = orm.Required(int)
