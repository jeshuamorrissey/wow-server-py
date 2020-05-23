from pony import orm

from database.constants import common
from database.db import db


class Languages(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(common.MultiEnumString)

    chr_races_backlink = orm.Set('ChrRaces', reverse='base_language')
