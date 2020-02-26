from database.world.game_object import unit
from typing import Dict, Any
from database.dbc import constants as c

from pony import orm


class Pet(unit.Unit):
    talent_points = orm.Required(int, default=0)

    def bytes_1(self) -> int:
        return super(Pet, self).bytes_1() | self.talent_points << 8

    def high_guid(self) -> c.HighGUID:
        return c.HighGUID.PET

    def faction_template(self) -> int:
        return self.summoner.faction_template()

    def update_fields(self) -> Dict[c.UpdateField, Any]:
        f = c.UnitFields
        fields = {
            f.PETNUMBER: self.entry(),
            f.PET_NAME_TIMESTAMP: 0,
            f.PETEXPERIENCE: 0,
            f.PETNEXTLEVELEXP: 1000,
        }

        return {**super(Pet, self).update_fields(), **fields}
