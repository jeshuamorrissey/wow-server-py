from pony import orm

from typing import Tuple, Dict, Any

from database.db import db
from database.dbc import constants as c
from database.world.game_object.game_object import GameObject
from database.world.enchantment import Enchantment


class ItemEnchantment(db.Entity):
    item = orm.Required('Item')
    enchantment = orm.Required('Enchantment')
    slot = orm.Required(c.EnchantmentSlot)

    orm.PrimaryKey(item, slot)


class Item(GameObject):
    base_item = orm.Required('ItemTemplate')

    creator = orm.Optional('Player')
    enchantments = orm.Set('ItemEnchantment')

    # Reverse mappings.
    container = orm.Optional('Container')
    equipped_by = orm.Optional('EquippedItem')
    in_backpack = orm.Optional('BackpackItem')

    def position(self) -> Tuple[float, float, float]:
        """Get the current position of the object.

        All objects either have a position, or have a parent who has a 
        position, so a result from this should always be possible.

        Returns:
            A 3-tuple of floats (x, y, z).
        """
        if self.equipped_by:
            return self.equipped_by.owner.position()
        elif self.in_backpack:
            return self.in_backpack.owner.position()
        raise RuntimeError(f'item {self.id} does not have an owner!')

    def enchantment_map(self) -> Dict[c.EnchantmentSlot, Enchantment]:
        return {ench.slot: ench.enchantment for ench in self.enchantments}

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

    def num_fields(self) -> int:
        return 0x06 + 0x2A

    def update_fields(self) -> Dict[c.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        f = c.ItemFields
        fields: Dict[c.UpdateField, Any] = {}

        if self.equipped_by:
            fields.update({
                f.OWNER: self.equipped_by.owner.guid,
                f.CONTAINED: self.equipped_by.owner.guid,
            })
        elif self.in_backpack:
            fields.update({
                f.OWNER: self.in_backpack.owner.guid,
                f.CONTAINED: self.in_backpack.owner.guid,
            })
        elif self.container:
            fields.update({
                f.OWNER: self.container.on_slot.owner.guid,
                f.CONTAINED: self.container.guid,
            })

        print(fields)

        fields.update({
            f.CREATOR: 0,
            f.CREATOR + 1: 0,
            f.GIFTCREATOR: 0,
            f.GIFTCREATOR + 1: 0,
            f.STACK_COUNT: 0,
            f.DURATION: 0,
            f.SPELL_CHARGES: 0,
            f.SPELL_CHARGES_01: 0,
            f.SPELL_CHARGES_02: 0,
            f.SPELL_CHARGES_03: 0,
            f.SPELL_CHARGES_04: 0,
            f.FLAGS: 0,
            # f.ENCHANTMENT: 0,  # TODO
            f.PROPERTY_SEED: 0,
            f.RANDOM_PROPERTIES_ID: 0,
            f.ITEM_TEXT_ID: 0,
            f.DURABILITY: 0,
            f.MAXDURABILITY: 0,
        })

        return {**super(Item, self).update_fields(), **fields}
