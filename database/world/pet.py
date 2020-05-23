import datetime
from typing import Any, Dict

from pony import orm

from database import enums

from . import unit


class Pet(unit.Unit):
    name_timestamp = orm.Required(datetime.datetime,
                                  default=lambda: datetime.datetime.now())
    talent_points = orm.Required(int, default=0)

    def bytes_1(self) -> int:
        return super(Pet, self).bytes_1() | self.talent_points << 8

    def high_guid(self) -> enums.HighGUID:
        return enums.HighGUID.PET

    def faction_template(self) -> int:
        return self.summoner.faction_template()

    def update_fields(self) -> Dict[enums.UpdateField, Any]:
        f = enums.UnitFields
        fields = {
            f.PETNUMBER: self.entry(),
            f.PET_NAME_TIMESTAMP: int(self.name_timestamp.timestamp()),
            f.PETEXPERIENCE: 0,
            f.PETNEXTLEVELEXP: 1000,
            f.TRAINING_POINTS: 10,
        }

        return {**super(Pet, self).update_fields(), **fields}
