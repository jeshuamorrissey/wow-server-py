from pony import orm

from database.constants import common
from database.db import db


class SkillLine(db.Entity):
    id = orm.PrimaryKey(int)
    category_id = orm.Required(int, unsigned=True)
    skill_costs_id = orm.Required(int)
    display_name = orm.Required(common.MultiEnumString)
    description = orm.Optional(common.MultiString)
    spell_icon = orm.Required(int)

    player_skill_backlink = orm.Set('PlayerSkill')
