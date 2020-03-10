from typing import Any, Dict, Optional, Tuple

from pony import orm

from database import game
from database.db import db
from database.world import enchantment

from . import game_object


class ItemEnchantment(db.Entity):
    item = orm.Required('Item')
    enchantment = orm.Required('Enchantment')
    slot = orm.Required(game.EnchantmentSlot)

    orm.PrimaryKey(item, slot)


class Item(game_object.GameObject):
    base_item = orm.Required('ItemTemplate')

    stack_count = orm.Optional(int)
    durability = orm.Required(int, default=0)
    creator = orm.Optional('Player')
    enchantments = orm.Set('ItemEnchantment')

    # Flags
    is_bound = orm.Required(bool, default=False)
    is_unlocked = orm.Required(bool, default=False)
    is_wrapped = orm.Required(bool, default=False)
    is_readable = orm.Required(bool, default=False)

    # Reverse mappings.
    container = orm.Optional('ContainerItem')
    equipped_by = orm.Optional('EquippedItem')
    in_backpack = orm.Optional('BackpackItem')
    in_bank = orm.Optional('BankItem')
    in_vendor_buyback = orm.Optional('VendorBuybackItem')
    in_keyring = orm.Optional('KeyringItem')

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

    def enchantment_map(self) -> Dict[game.EnchantmentSlot, enchantment.Enchantment]:
        return {ench.slot: ench.enchantment for ench in self.enchantments}

    #
    # Class Methods (should be overwritten in children).
    #
    @classmethod
    def New(cls, base_item: game.ItemTemplate, **kwargs) -> 'Item':
        return Item(
            base_item=base_item,
            durability=base_item.MaxDurability,
            stack_count=base_item.stackable,
            **kwargs,
        )

    def entry(self) -> Optional[int]:
        return self.base_item.entry

    def type_id(self) -> game.TypeID:
        return game.TypeID.ITEM

    def type_mask(self) -> game.TypeMask:
        return super(Item, self).type_mask() | game.TypeMask.ITEM

    def update_flags(self) -> game.UpdateFlags:
        return game.UpdateFlags.ALL

    def high_guid(self) -> game.HighGUID:
        return game.HighGUID.ITEM

    def num_fields(self) -> int:
        return 0x06 + 0x2A

    def update_fields(self) -> Dict[game.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        f = game.ItemFields
        fields: Dict[game.UpdateField, Any] = {}

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
                f.OWNER: self.container.container.on_slot.owner.guid,
                f.CONTAINED: self.container.container.guid,
            })

        # Encode the flags.
        flags = 0
        if self.is_bound:
            flags |= game.ItemFlags.BOUND
        if self.is_unlocked:
            flags |= game.ItemFlags.UNLOCKED
        if self.is_wrapped:
            flags |= game.ItemFlags.WRAPPED
        if self.is_readable:
            flags |= game.ItemFlags.READABLE

        fields.update({
            f.CREATOR: self.creator.guid if self.creator else 0,
            f.GIFTCREATOR: 0,
            f.GIFTCREATOR + 1: 0,
            f.STACK_COUNT: self.stack_count,
            f.DURATION: 0,
            f.SPELL_CHARGES: 0,
            f.SPELL_CHARGES_01: 0,
            f.SPELL_CHARGES_02: 0,
            f.SPELL_CHARGES_03: 0,
            f.SPELL_CHARGES_04: 0,
            f.FLAGS: flags,
            f.ENCHANTMENT: 0,
            f.PROPERTY_SEED: 0,
            f.RANDOM_PROPERTIES_ID: 0,
            f.ITEM_TEXT_ID: 0,
            f.DURABILITY: self.durability,
            f.MAXDURABILITY: self.base_item.MaxDurability,
        })

        return {**super(Item, self).update_fields(), **fields}
