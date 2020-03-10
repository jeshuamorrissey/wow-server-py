from typing import Any, Dict, Tuple

from pony import orm

from database import game
from database.db import db

from . import item


class ContainerItem(db.Entity):
    container = orm.Required('Container')
    slot = orm.Required(int)
    item = orm.Required('Item')

    orm.PrimaryKey(container, slot)


class Container(item.Item):
    items = orm.Set('ContainerItem')
    slots = orm.Required(int)

    # Reverse mappings.
    equipped_bag_backlink = orm.Optional('EquippedBag')
    bank_bag_backlink = orm.Optional('BankBag')

    def position(self) -> Tuple[float, float, float]:
        """Get the current position of the object.

        All objects either have a position, or have a parent who has a 
        position, so a result from this should always be possible.

        Returns:
            A 3-tuple of floats (x, y, z).
        """
        if self.equipped_bag_backlink:
            return self.equipped_bag_backlink.owner.position()
        return super(Container, self).position()

    #
    # Class Methods (should be overwritten in children).
    #
    @classmethod
    def New(cls, base_item: game.ItemTemplate, **kwargs) -> 'Container':
        return Container(
            base_item=base_item,
            durability=base_item.MaxDurability,
            stack_count=base_item.stackable,
            slots=base_item.ContainerSlots,
            **kwargs,
        )

    def type_id(self) -> game.TypeID:
        return game.TypeID.CONTAINER

    def type_mask(self) -> game.TypeMask:
        return super(Container, self).type_mask() | game.TypeMask.CONTAINER

    def update_flags(self) -> game.UpdateFlags:
        return game.UpdateFlags.ALL

    def high_guid(self) -> game.HighGUID:
        return game.HighGUID.CONTAINER

    def num_fields(self) -> int:
        return 0x06 + 0x2A + 0x3A

    def update_fields(self) -> Dict[game.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        fields = {
            game.ContainerFields.NUM_SLOTS: self.slots,
        }

        for item in self.items:
            fields[game.ContainerFields.SLOT_1 + (item.slot * 2)] = item.item.guid

        return {**super(Container, self).update_fields(), **fields}
