from pony import orm

from database.constants import common
from database.db import db


class AuctionHouse(db.Entity):
    id = orm.PrimaryKey(int)
    faction = orm.Required('Faction', reverse='auction_house_backlink')
    deposit_rate = orm.Required(int)
    consignment_rate = orm.Required(int)
    name = orm.Required(common.MultiEnumString)
