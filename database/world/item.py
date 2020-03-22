from typing import Any, Dict, Optional, Tuple

from pony import orm

from database import enums, game
from database.db import db
from database.world import enchantment

from . import game_object


class ItemEnchantment(db.Entity):
    item = orm.Required('Item')
    enchantment = orm.Required('Enchantment')
    slot = orm.Required(enums.EnchantmentSlot)

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
    in_inventory = orm.Optional('InventoryItem')

    # equipped_by = orm.Optional('EquippedItem')
    # in_backpack = orm.Optional('BackpackItem')
    # in_bank = orm.Optional('BankItem')
    # in_vendor_buyback = orm.Optional('VendorBuybackItem')
    # in_keyring = orm.Optional('KeyringItem')

    def can_equip_to_slot(self, slot: enums.EquipmentSlot):
        self_it = self.base_item.InventoryType
        it = enums.InventoryType
        es = enums.EquipmentSlot
        if slot == es.HEAD:
            return self_it in {it.HEAD}
        elif slot == es.NECK:
            return self_it in {it.NECK}
        elif slot == es.SHOULDERS:
            return self_it in {it.SHOULDERS}
        elif slot == es.BODY:
            return self_it in {it.BODY, it.ROBE}
        elif slot == es.CHEST:
            return self_it in {it.CHEST}
        elif slot == es.WAIST:
            return self_it in {it.WAIST}
        elif slot == es.LEGS:
            return self_it in {it.LEGS}
        elif slot == es.FEET:
            return self_it in {it.FEET}
        elif slot == es.WRISTS:
            return self_it in {it.WRISTS}
        elif slot == es.HANDS:
            return self_it in {it.HANDS}
        elif slot == es.FINGER1:
            return self_it in {it.FINGER}
        elif slot == es.FINGER2:
            return self_it in {it.FINGER}
        elif slot == es.TRINKET1:
            return self_it in {it.TRINKET}
        elif slot == es.TRINKET2:
            return self_it in {it.TRINKET}
        elif slot == es.BACK:
            return self_it in {it.CLOAK}
        elif slot == es.MAIN_HAND:
            return self_it in {it._2HWEAPON, it.WEAPONMAINHAND, it.WEAPON}
        elif slot == es.OFF_HAND:
            return self_it in {it.SHIELD, it.WEAPONOFFHAND, it.HOLDABLE, it.RELIC}
        elif slot == es.RANGED:
            return self_it in {it.THROWN, it.RANGEDRIGHT, it.RANGED}
        elif slot == es.TABARD:
            return self_it in {it.TABARD}
        return False

    def position(self) -> Tuple[float, float, float]:
        """Get the current position of the object.

        All objects either have a position, or have a parent who has a 
        position, so a result from this should always be possible.

        Returns:
            A 3-tuple of floats (x, y, z).
        """
        if self.container:
            return self.container.container.position()
        elif self.in_inventory:
            return self.in_inventory.owner.position()
        raise RuntimeError(f'item {self.id} ({self.base_item.name}) does not have an owner!')

    def enchantment_map(self) -> Dict[enums.EnchantmentSlot, enchantment.Enchantment]:
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

    def type_id(self) -> enums.TypeID:
        return enums.TypeID.ITEM

    def type_mask(self) -> enums.TypeMask:
        return super(Item, self).type_mask() | enums.TypeMask.ITEM

    def update_flags(self) -> enums.UpdateFlags:
        return enums.UpdateFlags.ALL

    def high_guid(self) -> enums.HighGUID:
        return enums.HighGUID.ITEM

    def num_fields(self) -> int:
        return 0x06 + 0x2A

    def update_fields(self) -> Dict[enums.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        f = enums.ItemFields
        fields: Dict[enums.UpdateField, Any] = {}

        if self.in_inventory:
            fields.update({
                f.OWNER: self.in_inventory.owner.guid,
                f.CONTAINED: self.in_inventory.owner.guid,
            })
        elif self.container:
            fields.update({
                f.OWNER: self.container.container.in_inventory.owner.guid,
                f.CONTAINED: self.container.container.guid,
            })

        # Encode the flags.
        flags = 0
        if self.is_bound:
            flags |= enums.ItemFlags.BOUND
        if self.is_unlocked:
            flags |= enums.ItemFlags.UNLOCKED
        if self.is_wrapped:
            flags |= enums.ItemFlags.WRAPPED
        if self.is_readable:
            flags |= enums.ItemFlags.READABLE

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
