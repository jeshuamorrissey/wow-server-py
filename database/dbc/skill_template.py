import enum

from pony import orm

from typing import Tuple

from database.db import db
from database.dbc import constants as c


class SkillTemplate(db.Entity):
    id = orm.PrimaryKey(int, auto=True, min=10)

    name = orm.Required(str)

    skill_instances = orm.Set('PlayerSkill')