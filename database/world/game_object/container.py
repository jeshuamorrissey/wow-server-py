from pony import orm

from database.dbc import constants as c
from database.world.game_object.item import Item


class Container(Item):
    # Reverse mappings.
    on_slot = orm.Optional('EquippedBag')

    #
    # Class Methods (should be overwritten in children).
    #
    def type_id(self) -> c.TypeID:
        return c.TypeID.CONTAINER

    def type_mask(self) -> c.TypeMask:
        return super(Container, self).type_mask() | c.TypeMask.CONTAINER

    def update_flags(self) -> c.UpdateFlags:
        return c.UpdateFlags.ALL

    def high_guid(self) -> c.HighGUID:
        return c.HighGUID.CONTAINER
