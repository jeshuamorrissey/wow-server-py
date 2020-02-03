from pony import orm

from database.dbc import constants as c
from database.world.game_object.game_object import GameObject


class Item(GameObject):
    base_item = orm.Required('ItemTemplate')

    # Reverse mappings.
    equipped_by = orm.Optional('EquippedItem')
    in_backpack = orm.Optional('BackpackItem')

    #
    # Class Methods (should be overwritten in children).
    #
    def type_id(self) -> c.TypeID:
        return c.TypeID.ITEM

    def type_mask(self) -> c.TypeMask:
        return super(Item, self).type_mask() | c.TypeMask.ITEM

    def update_flags(self) -> c.UpdateFlags:
        return c.UpdateFlags.ALL

    def high_guid(self) -> c.HighGUID:
        return c.HighGUID.ITEM
