import datetime
import time
from typing import Dict, Text, Any, Tuple

from pony import orm

from collections import defaultdict

from database.db import db
from database.dbc import constants as c
from database.dbc.char_start_outfit import CharStartOutfit
from database.dbc.chr_start_locations import ChrStartLocation
from database.dbc.item_template import ItemTemplate
from database.world.account import Account
from database.world.game_object import unit
from database.world.game_object.item import Item
from database.world.realm import Realm


class EquippedItem(db.Entity):
    """Mapping table to store details about which items are equipped."""
    owner = orm.Required('Player')
    slot = orm.Required(c.EquipmentSlot)
    item = orm.Required('Item')

    orm.PrimaryKey(owner, slot)


class BackpackItem(db.Entity):
    """Mapping table to store details about which items are in the backpack.

    The backpack is the default bag you always have available.
    """
    owner = orm.Required('Player')
    slot = orm.Required(int, min=0, max=15)
    item = orm.Required('Item')

    orm.PrimaryKey(owner, slot)


class EquippedBag(db.Entity):
    """Mapping table to store details about which bags are equipped."""
    owner = orm.Required('Player')
    slot = orm.Required(int, min=0, max=3)
    container = orm.Required('Container')

    orm.PrimaryKey(owner, slot)


class BankItem(db.Entity):
    owner = orm.Required('Player')
    slot = orm.Required(int, min=0, max=23)
    item = orm.Required('Item')

    orm.PrimaryKey(owner, slot)


class BankBag(db.Entity):
    owner = orm.Required('Player')
    slot = orm.Required(int, min=0, max=5)
    container = orm.Required('Container')

    orm.PrimaryKey(owner, slot)


class VendorBuybackItem(db.Entity):
    owner = orm.Required('Player')
    slot = orm.Required(int, min=0, max=11)
    item = orm.Required('Item')

    orm.PrimaryKey(owner, slot)


class KeyringItem(db.Entity):
    owner = orm.Required('Player')
    slot = orm.Required(int, min=0, max=31)
    item = orm.Required('Item')

    orm.PrimaryKey(owner, slot)


class Player(unit.Unit):
    # General character information.
    account = orm.Required('Account')
    realm = orm.Required('Realm')
    name = orm.Required(str, unique=True)
    last_login = orm.Optional(datetime.datetime)

    # Relationships.
    guild_membership = orm.Optional('GuildMembership')

    # Player location information.
    zone = orm.Required(int)
    map = orm.Required(int)

    # Inventory.
    equipment = orm.Set(EquippedItem)
    backpack = orm.Set(BackpackItem)
    bags = orm.Set(EquippedBag)
    bank = orm.Set(BankItem)
    bank_bags = orm.Set(BankBag)
    vendor_buyback = orm.Set(VendorBuybackItem)
    keyring = orm.Set(KeyringItem)

    quests = orm.Set('Quest')

    # Game-object specific information.
    skin_color = orm.Required(int, default=0)
    face = orm.Required(int, default=0)
    hair_style = orm.Required(int, default=0)
    hair_color = orm.Required(int, default=0)
    feature = orm.Required(int, default=0)

    # Player flags.
    is_group_leader = orm.Required(bool, default=False)
    is_afk = orm.Required(bool, default=False)
    is_dnd = orm.Required(bool, default=False)
    is_gm = orm.Required(bool, default=False)
    is_ghost = orm.Required(bool, default=False)
    is_ffa_pvp = orm.Required(bool, default=False)
    is_contested_pvp = orm.Required(bool, default=False)
    is_in_pvp = orm.Required(bool, default=False)
    hide_helm = orm.Required(bool, default=False)
    hide_cloak = orm.Required(bool, default=False)
    has_partial_play_time = orm.Required(bool, default=False)
    has_no_play_time = orm.Required(bool, default=False)
    in_sanctuary = orm.Required(bool, default=False)
    on_taxi_benchmark = orm.Required(bool, default=False)
    has_pvp_timer = orm.Required(bool, default=False)

    # Reverse mappings.
    created_items = orm.Set(Item)
    dual_arbiter = orm.Optional('Player', reverse='dual_arbiter')

    def equipment_map(self) -> Dict[c.EquipmentSlot, Item]:
        """Return a mapping of equipment slot --> equipped item.
        
        This is useful in situations where we have to fully specify the
        equipment (even if there is no equipment).

        Returns:
            A mapping from equipment slot --> item equipped in that slot.
        """
        return {eq.slot: eq.item for eq in self.equipment}

    def player_flags(self) -> c.PlayerFlags:
        f = c.PlayerFlags.NONE
        if self.is_group_leader:
            f |= c.PlayerFlags.GROUP_LEADER
        if self.is_afk:
            f |= c.PlayerFlags.AFK
        if self.is_dnd:
            f |= c.PlayerFlags.DND
        if self.is_gm:
            f |= c.PlayerFlags.GM
        if self.is_ghost:
            f |= c.PlayerFlags.GHOST
        if self.is_resting:
            f |= c.PlayerFlags.RESTING
        if self.is_ffa_pvp:
            f |= c.PlayerFlags.FFA_PVP
        if self.is_contested_pvp:
            f |= c.PlayerFlags.CONTESTED_PVP
        if self.is_in_pvp:
            f |= c.PlayerFlags.IN_PVP
        if self.hide_helm:
            f |= c.PlayerFlags.HIDE_HELM
        if self.hide_cloak:
            f |= c.PlayerFlags.HIDE_CLOAK
        if self.has_partial_play_time:
            f |= c.PlayerFlags.PARTIAL_PLAY_TIME
        if self.has_no_play_time:
            f |= c.PlayerFlags.NO_PLAY_TIME
        if self.in_sanctuary:
            f |= c.PlayerFlags.SANCTUARY
        if self.on_taxi_benchmark:
            f |= c.PlayerFlags.TAXI_BENCHMARK
        if self.has_pvp_timer:
            f |= c.PlayerFlags.PVP_TIMER

        return f

    def visible_item_fields(self, slot: c.EquipmentSlot, item: Item) -> Dict[c.UpdateField, Any]:
        fields_start = c.PlayerFields.VISIBLE_ITEM_START + (slot * 12)
        if item:
            enchantments = item.enchantment_map()
            fields = {}
            for ench_slot in c.EnchantmentSlot:
                ench = enchantments.get(ench_slot)
                if ench:
                    fields[fields_start + 3 + ench_slot] = ench.id
                else:
                    fields[fields_start + 3 + ench_slot] = 0

            creator_guid = item.creator.guid if item.creator else 0
            fields.update({
                fields_start + 0: creator_guid,
                fields_start + 2: item.entry(),
                fields_start + 10: 0,  # TODO: item enchantments
                fields_start + 11: 0,  # TODO: always 0 in server?
            })

            return fields

        return {f: 0 for f in range(fields_start, fields_start + 11 + 1)}

    def inventory_fields(self, slot: c.EquipmentSlot, item: Item) -> Dict[c.UpdateField, Any]:
        field = c.PlayerFields.INVENTORY_START + (slot * 2)
        if item:
            return {field: item.guid}
        return {field: 0}

    @classmethod
    def New(
            cls,
            account: Account,
            realm: Realm,
            name: Text,
            race: c.Race,
            class_: c.Class,
            gender: c.Gender,
            **kwargs,
    ) -> 'Player':
        """Create a new player and return it.

        Args:
            account: The account the player belongs to.
            realm: The realm the player resides on.
            name: The player's name.
            race: The player's race.
            class_: The player's class.
            gender: The player's gender.
            **kwargs: Additional arguments to pass to the Player constructor.

        Returns:
            The newly created character.
        """
        starting_location = ChrStartLocation.get(race=race)
        starting_items = CharStartOutfit.get(race=race, class_=class_, gender=gender)

        team = c.Team.ALLIANCE
        if race in (c.Race.ORC, c.Race.UNDEAD, c.Race.TAUREN, c.Race.TROLL):
            team = c.Team.HORDE

        player = Player(
            account=account,
            realm=realm,
            name=name,
            level=1,
            race=race,
            class_=class_,
            gender=gender,
            team=team,
            x=starting_location.x,
            y=starting_location.y,
            z=starting_location.z,
            o=starting_location.o,
            zone=starting_location.zone,
            map=starting_location.map,
            **kwargs,
        )

        for equipment in starting_items.equipment:
            EquippedItem(
                owner=player,
                slot=c.EquipmentSlot[equipment['equipment_slot']],
                item=Item.New(ItemTemplate[equipment['entry']]),
            )

        for i, entry in enumerate(starting_items.items):
            BackpackItem(
                owner=player,
                slot=i,
                item=Item.New(ItemTemplate[entry]),
            )

        return player

    #
    # Class Methods (should be overwritten in children).
    #
    def type_id(self) -> c.TypeID:
        return c.TypeID.PLAYER

    def type_mask(self) -> c.TypeMask:
        return super(Player, self).type_mask() | c.TypeMask.PLAYER

    def high_guid(self) -> c.HighGUID:
        return c.HighGUID.PLAYER

    def num_fields(self) -> int:
        return 0x06 + 0xB6 + 0x446

    def calculate_attack_time(self, slot: c.EquipmentSlot) -> int:
        equipment = self.equipment_map()

        base = 1000 if slot == c.EquipmentSlot.MAIN_HAND else 0
        if slot in equipment:
            base = equipment[slot].base_item.delay

        return base

    def calculate_damage(self, slot: c.EquipmentSlot) -> Tuple[float, float]:
        equipment = self.equipment_map()

        base = 1.0, 1.0
        if slot in equipment:
            base = equipment[slot].base_item.dmg(0)  # TODO: #define this?

        return base

    def calculate_cast_speed_mod(self) -> float:
        return 1.0

    def calculate_armor(self) -> int:
        return 0

    def calculate_holy_resistance(self) -> int:
        return 0

    def calculate_fire_resistance(self) -> int:
        return 0

    def calculate_nature_resistance(self) -> int:
        return 0

    def calculate_frost_resistance(self) -> int:
        return 0

    def calculate_shadow_resistance(self) -> int:
        return 0

    def calculate_arcane_resistance(self) -> int:
        return 0

    def calculate_melee_attack_power(self) -> int:
        return self.strength * 5

    def calculate_ranged_attack_power(self) -> int:
        return self.agility * 5

    def update_fields(self) -> Dict[c.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        f = c.PlayerFields
        uf = c.UnitFields
        fields: Dict[c.UpdateField, Any] = defaultdict(lambda: 0)

        equipment = self.equipment_map()

        # Populate fields for virtual items (i.e. how sheathed items should
        # be displayed).
        if self.sheathed_state == c.SheathedState.MELEE:
            if c.EquipmentSlot.MAIN_HAND in equipment:
                fields.update(
                    self.virtual_item_fields(
                        c.EquipmentSlot.MAIN_HAND,
                        equipment[c.EquipmentSlot.MAIN_HAND].base_item,
                    ))

            if c.EquipmentSlot.OFF_HAND in equipment:
                fields.update(
                    self.virtual_item_fields(
                        c.EquipmentSlot.OFF_HAND,
                        equipment[c.EquipmentSlot.OFF_HAND].base_item,
                    ))

        elif self.sheathed_state == c.SheathedState.RANGED:
            if c.EquipmentSlot.RANGED in equipment:
                fields.update(
                    self.virtual_item_fields(
                        c.EquipmentSlot.RANGED,
                        equipment[c.EquipmentSlot.RANGED].base_item,
                    ))

        # Populate equipment fields.
        for equipment_slot in c.EquipmentSlot:
            item = equipment.get(equipment_slot)
            fields.update(self.visible_item_fields(equipment_slot, item))
            fields.update(self.inventory_fields(equipment_slot, item))

        # Populate backpack fields.
        for backpack_item in self.backpack:
            fields[f.PACK_SLOT_1 + (backpack_item.slot * 2)] = backpack_item.item.guid

        for bag in self.bags:
            fields[f.BAG_SLOT_1 + (bag.slot * 2)] = bag.container.guid

        for bank_item in self.bank:
            fields[f.BANK_SLOT_1 + (bank_item.slot * 2)] = bank_item.item.guid

        for bank_bag in self.bank_bags:
            fields[f.BANKBAG_SLOT_1 + (bank_bag.slot * 2)] = bank_bag.container.guid

        for vendor_buyback_item in self.vendor_buyback:
            fields[f.VENDORBUYBACK_SLOT_1 + (vendor_buyback_item.slot * 2)] = vendor_buyback_item.item.guid

        for keyring_item in self.keyring:
            fields[f.KEYRING_SLOT_1 + (keyring_item.slot * 2)] = keyring_item.item.guid

        fields.update({
            uf.BASEATTACKTIME: self.calculate_attack_time(c.EquipmentSlot.MAIN_HAND),
            uf.OFFHANDATTACKTIME: self.calculate_attack_time(c.EquipmentSlot.OFF_HAND),
            uf.RANGEDATTACKTIME: self.calculate_attack_time(c.EquipmentSlot.RANGED),
            uf.MINDAMAGE: self.calculate_damage(c.EquipmentSlot.MAIN_HAND)[0],
            uf.MAXDAMAGE: self.calculate_damage(c.EquipmentSlot.MAIN_HAND)[1],
            uf.MINOFFHANDDAMAGE: self.calculate_damage(c.EquipmentSlot.OFF_HAND)[0],
            uf.MAXOFFHANDDAMAGE: self.calculate_damage(c.EquipmentSlot.OFF_HAND)[1],
            uf.MINRANGEDDAMAGE: self.calculate_damage(c.EquipmentSlot.RANGED)[0],
            uf.MAXRANGEDDAMAGE: self.calculate_damage(c.EquipmentSlot.RANGED)[1],
            uf.ATTACK_POWER: self.calculate_melee_attack_power(),
            uf.RANGED_ATTACK_POWER: self.calculate_ranged_attack_power(),
            uf.COMBATREACH: 1.5,  # TODO: make this config
            uf.ARMOR: self.calculate_armor(),
            uf.HOLY_RESISTANCE: self.calculate_holy_resistance(),
            uf.FIRE_RESISTANCE: self.calculate_fire_resistance(),
            uf.NATURE_RESISTANCE: self.calculate_nature_resistance(),
            uf.FROST_RESISTANCE: self.calculate_frost_resistance(),
            uf.SHADOW_RESISTANCE: self.calculate_shadow_resistance(),
            uf.ARCANE_RESISTANCE: self.calculate_arcane_resistance(),
        })

        if self.guild_membership:
            fields.update({
                f.GUILDID: self.guild_membership.guild.id,
                f.GUILDRANK: self.guild_membership.rank,
                f.GUILD_TIMESTAMP: 0,
            })
        else:
            fields.update({
                f.GUILDID: 0,
                f.GUILDRANK: 0,
                f.GUILD_TIMESTAMP: 0,
            })

        # NOTE: Not implementing PvP fields, because this is meant to be single player.
        fields.update({
            f.DUEL_ARBITER: 0,
            f.DUEL_TEAM: 0,
        })

        # Quest updates.
        for i, quest in enumerate(self.quests):
            start_field = f.QUEST_LOG_1_1 + (i * 3)
            fields.update({
                start_field + 0: quest.base_quest.id,
                start_field + 1: quest.flags(),
                start_field + 2: quest.due - int(time.time()) if quest.due else 0,
            })

        fields.update({
            f.FLAGS: self.player_flags(),
            f.BYTES: self.skin_color | self.face << 8 | self.hair_style << 16 | self.hair_color << 24,
            f.BYTES_2: self.feature,
            f.BYTES_3: self.gender,
            f.FARSIGHT: 0,
            f.COMBO_TARGET: 0,
            f.XP: 0,
            f.NEXT_LEVEL_XP: 0,
            f.SKILL_INFO_1_1: 0,
            f.CHARACTER_POINTS1: 0,
            f.CHARACTER_POINTS2: 0,
            f.TRACK_CREATURES: 0,
            f.TRACK_RESOURCES: 0,
            f.BLOCK_PERCENTAGE: 0,
            f.DODGE_PERCENTAGE: 0,
            f.PARRY_PERCENTAGE: 0,
            f.CRIT_PERCENTAGE: 0,
            f.RANGED_CRIT_PERCENTAGE: 0,
            f.EXPLORED_ZONES_1: 0,
            f.REST_STATE_EXPERIENCE: 0,
            f.COINAGE: 0,
            f.POSSTAT0: 0,
            f.POSSTAT1: 0,
            f.POSSTAT2: 0,
            f.POSSTAT3: 0,
            f.POSSTAT4: 0,
            f.NEGSTAT0: 0,
            f.NEGSTAT1: 0,
            f.NEGSTAT2: 0,
            f.NEGSTAT3: 0,
            f.NEGSTAT4: 0,
            f.RESISTANCEBUFFMODSPOSITIVE: 0,
            f.RESISTANCEBUFFMODSNEGATIVE: 0,
            f.MOD_DAMAGE_DONE_POS: 0,
            f.MOD_DAMAGE_DONE_NEG: 0,
            f.MOD_DAMAGE_DONE_PCT: 0,
            f.BYTES: 0,
            f.AMMO_ID: 0,
            f.SELF_RES_SPELL: 0,
            f.PVP_MEDALS: 0,
            f.BUYBACK_PRICE_1: 0,
            f.BUYBACK_PRICE_LAST: 0,
            f.BUYBACK_TIMESTAMP_1: 0,
            f.BUYBACK_TIMESTAMP_LAST: 0,
            f.SESSION_KILLS: 0,
            f.YESTERDAY_KILLS: 0,
            f.LAST_WEEK_KILLS: 0,
            f.THIS_WEEK_KILLS: 0,
            f.THIS_WEEK_CONTRIBUTION: 0,
            f.LIFETIME_HONORABLE_KILLS: 0,
            f.LIFETIME_DISHONORABLE_KILLS: 0,
            f.YESTERDAY_CONTRIBUTION: 0,
            f.LAST_WEEK_CONTRIBUTION: 0,
            f.LAST_WEEK_RANK: 0,
            f.BYTES2: 0,
            f.WATCHED_FACTION_INDEX: 0,
            f.COMBAT_RATING_1: 0,
        })

        return {**super(Player, self).update_fields(), **fields}
