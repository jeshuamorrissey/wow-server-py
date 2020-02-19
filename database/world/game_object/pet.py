from database.world.game_object import unit
from typing import Dict, Any
from database.dbc import constants as c


class Pet(unit.Unit):
    def high_guid(self) -> c.HighGUID:
        return c.HighGUID.PET

    def update_fields(self) -> Dict[c.UpdateField, Any]:
        f = c.UnitFields
        fields = {
            f.PETNUMBER: self.entry,
            f.PET_NAME_TIMESTAMP: 0,
            f.PETEXPERIENCE: 0,
            f.PETNEXTLEVELEXP: 1000,
        }

        return {**super(Pet, self).update_fields(), **fields}
