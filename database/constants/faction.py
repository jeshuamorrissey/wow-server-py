from pony import orm

from database.constants import common
from database.db import db


class Faction(db.Entity):
    id = orm.PrimaryKey(int)
    reputation_index = orm.Required(int, unsigned=True)
    reputation_race_mask1 = orm.Required(int, unsigned=True)
    reputation_race_mask2 = orm.Required(int, unsigned=True)
    reputation_race_mask3 = orm.Required(int, unsigned=True)
    reputation_race_mask4 = orm.Required(int, unsigned=True)
    reputation_class_mask1 = orm.Required(int, unsigned=True)
    reputation_class_mask2 = orm.Required(int, unsigned=True)
    reputation_class_mask3 = orm.Required(int, unsigned=True)
    reputation_class_mask4 = orm.Required(int, unsigned=True)
    reputation_base1 = orm.Required(int, unsigned=True)
    reputation_base2 = orm.Required(int, unsigned=True)
    reputation_base3 = orm.Required(int, unsigned=True)
    reputation_base4 = orm.Required(int, unsigned=True)
    reputation_flags1 = orm.Required(int, unsigned=True)
    reputation_flags2 = orm.Required(int, unsigned=True)
    reputation_flags3 = orm.Required(int, unsigned=True)
    reputation_flags4 = orm.Required(int, unsigned=True)
    parent_faction = orm.Optional('Faction', reverse='parent_faction_backlink')
    name = orm.Required(common.MultiEnumString)
    description = orm.Optional(common.MultiString)

    parent_faction_backlink = orm.Set('Faction', reverse='parent_faction')
    auction_house_backlink = orm.Set('AuctionHouse', reverse='faction')
    chr_races_backlink = orm.Set('ChrRaces', reverse='faction')
    player_backlink = orm.Set('Player')
