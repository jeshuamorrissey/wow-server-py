from pony import orm

from database.db import db


class UnitModelInfo(db.Entity):
    id = orm.PrimaryKey(int)
    bounding_radius = orm.Required(float)
    combat_reach = orm.Required(float)
    gender = orm.Required(int)
    other_gender = orm.Optional('UnitModelInfo', reverse='other_gender')
    other_team = orm.Optional('UnitModelInfo', reverse='other_team')

    unit_1_backlink = orm.Set('UnitTemplate', reverse='ModelId1')
    unit_2_backlink = orm.Set('UnitTemplate', reverse='ModelId2')
    unit_3_backlink = orm.Set('UnitTemplate', reverse='ModelId3')
    unit_4_backlink = orm.Set('UnitTemplate', reverse='ModelId4')
    chr_races_male_id_backlink = orm.Set('ChrRaces',
                                         reverse='male_display_info')
    chr_races_female_id_backlink = orm.Set('ChrRaces',
                                           reverse='female_display_info')
