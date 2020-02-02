from pony import orm

from database.dbc import constants as c
from database.dbc.chr_start_locations import ChrStartLocation


@orm.db_session
def LoadDBC():
    # yapf: disable
    ChrStartLocation(race=c.Race.HUMAN, map=0, zone=12, x=-8949.95, y=-132.493, z=83.5312, o=0.0)
    ChrStartLocation(race=c.Race.ORC, map=1, zone=14, x=-618.518, y=-4251.67, z=38.718, o=0.0)
    ChrStartLocation(race=c.Race.DWARF, map=0, zone=1, x=-6240.32, y=331.033, z=382.758, o=6.17716)
    ChrStartLocation(race=c.Race.NIGHTELF, map=1, zone=141, x=10311.3, y=832.463, z=1326.41, o=5.69632)
    ChrStartLocation(race=c.Race.UNDEAD, map=0, zone=85, x=1676.71, y=1678.31, z=121.67, o=2.70526)
    ChrStartLocation(race=c.Race.TAUREN, map=1, zone=215, x=-2917.58, y=-257.98, z=52.9968, o=0.0)
    ChrStartLocation(race=c.Race.GNOME, map=0, zone=1, x=-6240.32, y=331.033, z=382.758, o=0.0)
    ChrStartLocation(race=c.Race.TROLL, map=1, zone=14, x=-618.518, y=-4251.67, z=38.718, o=0.0)

    # yapf: enable
