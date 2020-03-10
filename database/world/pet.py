from typing import Any, Dict

from pony import orm

from database import game

from . import unit


class Pet(unit.Unit):
    talent_points = orm.Required(int, default=0)

    def bytes_1(self) -> int:
        return super(Pet, self).bytes_1() | self.talent_points << 8

    def high_guid(self) -> game.HighGUID:
        return game.HighGUID.PET

    def faction_template(self) -> int:
        return self.summoner.faction_template()

    def update_fields(self) -> Dict[game.UpdateField, Any]:
        f = game.UnitFields
        fields = {
            f.PETNUMBER: self.entry(),
            f.PET_NAME_TIMESTAMP: 0,
            f.PETEXPERIENCE: 0,
            f.PETNEXTLEVELEXP: 1000,
            f.TRAINING_POINTS: 10,
        }

        return {**super(Pet, self).update_fields(), **fields}
