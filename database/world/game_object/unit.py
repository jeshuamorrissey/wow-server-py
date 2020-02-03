from pony import orm

from database.dbc import constants as c
from database.world.game_object.game_object import GameObject


class Unit(GameObject):
    level = orm.Required(int, min=1)
    race = orm.Required(c.Race)
    class_ = orm.Required(c.Class)
    gender = orm.Required(c.Gender)

    # For NPC units, they will link to a template.
    base_unit = orm.Optional('UnitTemplate')

    # For pets, they will have a master.
    master = orm.Optional('Player')

    # Unit location information.
    x = orm.Required(float)
    y = orm.Required(float)
    z = orm.Required(float)
    o = orm.Required(float)

    #
    # Class Methods (should be overwritten in children).
    #
    def type_id(self) -> c.TypeID:
        return c.TypeID.UNIT

    def type_mask(self) -> c.TypeMask:
        return super(Unit, self).type_mask() | c.TypeMask.UNIT

    def update_flags(self) -> c.UpdateFlags:
        return c.UpdateFlags.ALL | c.UpdateFlags.LIVING | c.UpdateFlags.HAS_POSITION

    def high_guid(self) -> c.HighGUID:
        if self.master:
            return c.HighGUID.PET
        return c.HighGUID.UNIT
