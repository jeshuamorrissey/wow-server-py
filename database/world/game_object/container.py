from pony import orm

from typing import Tuple, Dict, Any

from database.dbc import constants as c
from database.world.game_object.item import Item


class Container(Item):
    # Reverse mappings.
    on_slot = orm.Optional('EquippedBag')

    def position(self) -> Tuple[float, float, float]:
        """Get the current position of the object.

        All objects either have a position, or have a parent who has a 
        position, so a result from this should always be possible.

        Returns:
            A 3-tuple of floats (x, y, z).
        """
        if self.on_slot:
            return self.on_slot.owner.position()
        return super(Container, self).position()

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

    def update_fields(self) -> Dict[c.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        fields = {
            c.ContainerFields.NUM_SLOTS: 0,
        }

        for slot_f in range(c.ContainerFields.SLOT_1,
                            c.ContainerFields.SLOT_LAST + 1, 2):
            fields[slot_f] = 0
            fields[slot_f + 1] = 0

        return {**super(Container, self).update_fields(), **fields}
