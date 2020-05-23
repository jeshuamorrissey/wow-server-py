from pony import orm

from database.constants import common
from database.db import db


class CreatureType(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(common.MultiEnumString)
    flags = orm.Required(int)

    chr_races_backlink = orm.Set('ChrRaces', reverse='creature_type')
