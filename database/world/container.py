from typing import Any, Dict, Optional, Tuple

from pony import orm

from database import common, enums, game
from database.db import db

from . import game_object, item


class ContainerItem(db.Entity, common.SlottedEntityMixin):
    container = orm.Required('Container')
    slot = orm.Required(int)
    item = orm.Optional('Item')

    def after_update(self):
        self.container.after_update()
        if self.item:
            self.item.after_update()

    def can_contain(self, item: Optional['item.Item']) -> bool:
        """Return true iff this slot can contain the given item."""
        return True

    orm.PrimaryKey(container, slot)


class Container(item.Item):
    items = orm.Set('ContainerItem')
    slots = orm.Required(int)

    def contents(self) -> Dict[int, ContainerItem]:
        return {ci.slot: ci for ci in self.items}

    #
    # Class Methods (should be overwritten in children).
    #
    @classmethod
    def New(cls, base_item: game.ItemTemplate, **kwargs) -> 'Container':
        container = Container(
            base_item=base_item,
            durability=base_item.MaxDurability,
            stack_count=base_item.stackable,
            slots=base_item.ContainerSlots,
            **kwargs,
        )

        for slot in range(container.slots):
            ContainerItem(container=container, slot=slot)

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
            enums.ContainerFields.NUM_SLOTS: self.slots,
        }

        for slot, ci in self.contents().items():
            if ci.item:
                fields[enums.ContainerFields.SLOT_1 + (slot * 2)] = ci.item.guid
            else:
                fields[enums.ContainerFields.SLOT_1 + (slot * 2)] = game_object.GUID(0)

        return {**super(Container, self).update_fields(), **fields}
