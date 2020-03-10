from typing import Any, Dict, Tuple

from pony import orm

from database.db import db

from database.dbc import constants as c
from database.world.game_object.item import Item
from database.dbc.item_template import ItemTemplate


class ContainerItem(db.Entity):
    container = orm.Required('Container')
    slot = orm.Required(int)
    item = orm.Required('Item')

    orm.PrimaryKey(container, slot)


class Container(Item):
    items = orm.Set('ContainerItem')
    slots = orm.Required(int)

    # Reverse mappings.
    on_slot = orm.Optional('EquippedBag')
    on_bank_slot = orm.Optional('BankBag')

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
    @classmethod
    def New(cls, base_item: ItemTemplate, **kwargs) -> 'Container':
        return Container(
            base_item=base_item,
            durability=base_item.MaxDurability,
            stack_count=base_item.stackable,
            slots=base_item.ContainerSlots,
            **kwargs,
        )

    def type_id(self) -> c.TypeID:
        return c.TypeID.CONTAINER

    def type_mask(self) -> c.TypeMask:
        return super(Container, self).type_mask() | c.TypeMask.CONTAINER

    def update_flags(self) -> c.UpdateFlags:
        return c.UpdateFlags.ALL

    def high_guid(self) -> c.HighGUID:
        return c.HighGUID.CONTAINER

    def num_fields(self) -> int:
        return 0x06 + 0x2A + 0x3A

    def update_fields(self) -> Dict[c.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        fields = {
            c.ContainerFields.NUM_SLOTS: self.slots,
        }

        for item in self.items:
            fields[c.ContainerFields.SLOT_1 + (item.slot * 2)] = item.item.guid

        return {**super(Container, self).update_fields(), **fields}
