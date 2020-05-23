from typing import Any, Dict, List, Optional, Tuple

from pony import orm

from database import enums, game
from database.db import db
from database.world import enchantment

from . import container, game_object


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
    in_inventory = orm.Optional('PlayerInventorySlot')
    in_container = orm.Optional('ContainerSlot')

    def equipment_slot(self) -> List[enums.EquipmentSlot]:
        it = enums.InventoryType
        inventory_type = self.base_item.InventoryType
        if inventory_type in {it.HEAD}:
            return [enums.EquipmentSlot.HEAD]
        if inventory_type in {it.NECK}:
            return [enums.EquipmentSlot.NECK]
        if inventory_type in {it.SHOULDERS}:
            return [enums.EquipmentSlot.SHOULDERS]
        if inventory_type in {it.BODY, it.ROBE}:
            return [enums.EquipmentSlot.BODY]
        if inventory_type in {it.CHEST}:
            return [enums.EquipmentSlot.CHEST]
        if inventory_type in {it.WAIST}:
            return [enums.EquipmentSlot.WAIST]
        if inventory_type in {it.LEGS}:
            return [enums.EquipmentSlot.LEGS]
        if inventory_type in {it.FEET}:
            return [enums.EquipmentSlot.FEET]
        if inventory_type in {it.WRISTS}:
            return [enums.EquipmentSlot.WRISTS]
        if inventory_type in {it.HANDS}:
            return [enums.EquipmentSlot.HANDS]
        if inventory_type in {it.FINGER}:
            return [enums.EquipmentSlot.FINGER1, enums.EquipmentSlot.FINGER2]
        if inventory_type in {it.TRINKET}:
            return [enums.EquipmentSlot.TRINKET1, enums.EquipmentSlot.TRINKET2]
        if inventory_type in {it.CLOAK}:
            return [enums.EquipmentSlot.BACK]
        if inventory_type in {it._2HWEAPON, it.WEAPONMAINHAND, it.WEAPON}:
            return [enums.EquipmentSlot.MAIN_HAND]
        if inventory_type in {
                it.SHIELD, it.WEAPONOFFHAND, it.HOLDABLE, it.RELIC
        }:
            return [enums.EquipmentSlot.OFF_HAND]
        if inventory_type in {it.THROWN, it.RANGEDRIGHT, it.RANGED}:
            return [enums.EquipmentSlot.RANGED]
        if inventory_type in {it.TABARD}:
            return [enums.EquipmentSlot.TABARD]
        return []

    def can_equip_to_slot(self, slot: enums.EquipmentSlot):
        return slot in self.equipment_slot()

    def position(self) -> Tuple[float, float, float]:
        """Get the current position of the object.

        All objects either have a position, or have a parent who has a 
        position, so a result from this should always be possible.

        Returns:
            A 3-tuple of floats (x, y, z).
        """
        if self.in_inventory:
            return self.in_inventory.player.position()
        if self.in_container:
            return self.in_container.container.position()
        raise RuntimeError(
            f'item {self.id} ({self.base_item.name}) does not have an owner!')

    def enchantment_map(
            self) -> Dict[enums.EnchantmentSlot, enchantment.Enchantment]:
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

        if self.in_container:
            fields.update({
                f.OWNER: self.in_container.container.in_inventory.player.guid,
                f.CONTAINED: self.in_container.container.guid,
            })
        elif self.in_inventory:
            fields.update({
                f.OWNER: self.in_inventory.player.guid,
                f.CONTAINED: self.in_inventory.player.guid,
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
