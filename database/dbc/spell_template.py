import enum

from pony import orm

from typing import Tuple

from database.db import db
from database.dbc import constants as c


class SpellTemplate(db.Entity):
    id = orm.PrimaryKey(int, auto=True, min=10)

    aura_state_modifier = orm.Required(c.AuraState, default=c.AuraState.NONE)

    aura_instances = orm.Set('Aura')