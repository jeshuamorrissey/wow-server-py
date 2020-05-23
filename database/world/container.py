from typing import Any, Dict, Optional, Tuple

from pony import orm

from database import common, enums, game
from database.db import db

from . import game_object
from .item import Item


class ContainerSlot(db.Entity):
    container = orm.Required('Container')
    slot = orm.Required(int)
    item = orm.Optional('Item')

    orm.PrimaryKey(container, slot)

    def after_update(self):
        print('ContainerSlot', self.container, self.item)
        self.container.after_update()
        if self.item:
            self.item.after_update()

    def can_contain(self, item: Optional[Item]) -> bool:
        if not item:
            return True

        # TODO: containers which can only hold certain items
        return True


class Container(Item):
    slots = orm.Set(ContainerSlot)

    def items(self) -> Dict[int, ContainerSlot]:
        return {slot.slot: slot for slot in self.slots}

    #
    # Class Methods (should be overwritten in children).
    #
    @classmethod
    def New(cls, base_item: game.ItemTemplate, **kwargs) -> 'Container':
        container = Container(
            base_item=base_item,
            durability=base_item.MaxDurability,
            stack_count=base_item.stackable,
            **kwargs,
        )

        for slot in range(base_item.ContainerSlots):
            ContainerSlot(container=container, slot=slot)

        return container

    def type_id(self) -> enums.TypeID:
        return enums.TypeID.CONTAINER

    def type_mask(self) -> enums.TypeMask:
        return super(Container, self).type_mask() | enums.TypeMask.CONTAINER

    def update_flags(self) -> enums.UpdateFlags:
        return enums.UpdateFlags.ALL

    def high_guid(self) -> enums.HighGUID:
        return enums.HighGUID.CONTAINER

    def num_fields(self) -> int:
        return 0x06 + 0x2A + 0x3A

    def update_fields(self) -> Dict[enums.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        fields = {
            enums.ContainerFields.NUM_SLOTS: len(self.slots),
        }

        for slot, ci in self.items().items():
            if ci.item:
                fields[enums.ContainerFields.SLOT_1 + (slot * 2)] = ci.item.guid
            else:
                fields[enums.ContainerFields.SLOT_1 +
                       (slot * 2)] = game_object.GUID(0)

        return {**super(Container, self).update_fields(), **fields}
