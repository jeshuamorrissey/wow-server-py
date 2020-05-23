import datetime
import time
from collections import defaultdict
from typing import Any, Dict, List, Optional, Text, Tuple

from pony import orm

from database import constants, enums, game
from database.db import db

from . import container, game_object, unit
from .account import Account
from .item import Item
from .realm import Realm


class PlayerInventorySlot(db.Entity):
    player = orm.Required('Player')
    slot = orm.Required(int, min=enums.InventorySlots.EQUIPMENT_START, max=enums.InventorySlots.KEYRING_END)
    item = orm.Optional('Item')

    orm.PrimaryKey(player, slot)

    def after_update(self):
        print('PlayerInventorySlot', self.player, self.item)
        self.player.after_update()
        if self.item:
            self.item.after_update()

    def can_contain(self, item: Optional[Item]) -> bool:
        if not item:
            return True

        s = enums.InventorySlots
        if s.EQUIPMENT_START <= self.slot < s.EQUIPMENT_END:
            equipment_slot = enums.EquipmentSlot(self.slot)
            if not item.can_equip_to_slot(equipment_slot):
                return False

        if (s.BAG_START <= self.slot < s.BAG_END or s.BANK_BAG_START <= self.slot < s.BANK_BAG_END):
            if not isinstance(item, container.Container):
                return False

        return True


class PlayerSkill(db.Entity):
    player = orm.Required('Player')
    skill = orm.Required(constants.SkillLine)

    level = orm.Required(int, default=0)
    bonus = orm.Required(int, default=0)

    def max_level(self) -> int:
        return self.player.level * 5

    def temp_bonus(self) -> int:
        return 5

    orm.PrimaryKey(player, skill)


class PlayerSpell(db.Entity):
    player = orm.Required('Player')
    spell = orm.Required(constants.Spell)

    orm.PrimaryKey(player, spell)


class PlayerActionButton(db.Entity):
    player = orm.Required('Player')
    slot = orm.Required(int)
    type = orm.Required(enums.ActionButtonType)
    action = orm.Required(int)

    orm.PrimaryKey(player, slot)


class PlayerMail(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    from_player = orm.Required('Player', reverse='received_mail')
    to_player = orm.Required('Player', reverse='sent_mail')

    content = orm.Required(str)


class Player(unit.Unit):
    # General character information.
    account = orm.Required('Account')
    realm = orm.Required('Realm')
    last_login = orm.Optional(datetime.datetime)
    xp = orm.Required(int, default=0)
    rested_xp = orm.Required(int, default=0)  # amount of rested XP bonus
    money = orm.Required(int, default=0)

    watched_faction = orm.Optional('Faction')

    tutorials = orm.Required(orm.Json, default=[False] * 256)

    inventory = orm.Set('PlayerInventorySlot')
    # professions = orm.Set(PlayerProfession)
    explored_zones = orm.Required(orm.IntArray, default=[])

    skills = orm.Set(PlayerSkill)
    spells = orm.Set(PlayerSpell)
    action_buttons = orm.Set(PlayerActionButton)

    received_mail = orm.Set(PlayerMail, reverse='from_player')
    sent_mail = orm.Set(PlayerMail, reverse='to_player')

    # Relationships.
    guild_membership = orm.Optional('GuildMembership')
    combo_target = orm.Optional('Player', reverse='combo_target_of')
    combo_target_of = orm.Set('Player', reverse='combo_target')
    combo_points = orm.Optional(int)

    # Player location information.
    zone = orm.Required(int)
    map = orm.Required(int)
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

    is_tracking_stealth = orm.Required(bool, default=False)
    has_release_timer = orm.Required(bool, default=False)
    has_no_release_window = orm.Required(bool, default=False)

    can_detect_amore_0 = orm.Required(bool, default=False)
    can_detect_amore_1 = orm.Required(bool, default=False)
    can_detect_amore_2 = orm.Required(bool, default=False)
    can_detect_amore_3 = orm.Required(bool, default=False)
    in_stealth = orm.Required(bool, default=False)
    has_invisibility_glow = orm.Required(bool, default=False)

    # Reverse mappings.
    created_items = orm.Set('Item')
    dual_arbiter = orm.Optional('Player', reverse='dual_arbiter')

    def swap_items(self, src_slot, dst_slot) -> enums.InventoryChangeError:
        pass

    def _inv_slice(self, start: int, end: int) -> Dict[int, PlayerInventorySlot]:
        return {pi.slot - start: pi for pi in self.inventory if pi.slot >= start and pi.slot < end}

    def equipment(self) -> Dict[enums.EquipmentSlot, PlayerInventorySlot]:
        return {
            enums.EquipmentSlot(s): i for s, i in self._inv_slice(enums.InventorySlots.EQUIPMENT_START,
                                                                  enums.InventorySlots.EQUIPMENT_END).items()
        }

    def bags(self) -> Dict[int, PlayerInventorySlot]:
        return self._inv_slice(enums.InventorySlots.BAG_START, enums.InventorySlots.BAG_END)

    def backpack(self) -> Dict[int, PlayerInventorySlot]:
        return self._inv_slice(enums.InventorySlots.BACKPACK_START, enums.InventorySlots.BACKPACK_END)

    def bank(self) -> Dict[int, PlayerInventorySlot]:
        return self._inv_slice(enums.InventorySlots.BANK_START, enums.InventorySlots.BANK_END)

    def bank_bags(self) -> Dict[int, PlayerInventorySlot]:
        return self._inv_slice(enums.InventorySlots.BANK_BAG_START, enums.InventorySlots.BANK_BAG_END)

    def buyback_items(self) -> Dict[int, Item]:
        return self._inv_slice(enums.InventorySlots.BUYBACK_START, enums.InventorySlots.BUYBACK_END)

    def keyring(self) -> Dict[int, Item]:
        return self._inv_slice(enums.InventorySlots.KEYRING_START, enums.InventorySlots.KEYRING_END)

    def tutorial_flags(self) -> List[int]:
        """Convert the tutorial flag list into a list of bytes."""
        result = [0] * 8
        for i in range(len(result)):
            for flag_idx, flag_val in enumerate(self.tutorials[i * 32:i * 32 + 32]):
                if flag_val:
                    result[i] |= (1 << (flag_idx % 32))

        return result

    def get_item(self, bag_slot: int, slot: int):
        """Get an item from a given slot within some bag.

        The bag is an absolute value which corresponds to one of the
        many bag slots. The slot is the position of the item within
        that bag.
        """
        if bag_slot == 255:
            return PlayerInventorySlot.get(player=self, slot=slot)
        return PlayerInventorySlot.get(player=self, slot=bag_slot).item.items()[slot]

    def player_flags(self) -> enums.PlayerFlags:
        f = enums.PlayerFlags.NONE
        if self.is_group_leader:
            f |= enums.PlayerFlags.GROUP_LEADER
        if self.is_afk:
            f |= enums.PlayerFlags.AFK
        if self.is_dnd:
            f |= enums.PlayerFlags.DND
        if self.is_gm:
            f |= enums.PlayerFlags.GM
        if self.is_ghost:
            f |= enums.PlayerFlags.GHOST
        if self.is_resting:
            f |= enums.PlayerFlags.RESTING
        if self.is_ffa_pvp:
            f |= enums.PlayerFlags.FFA_PVP
        if self.is_contested_pvp:
            f |= enums.PlayerFlags.CONTESTED_PVP
        if self.is_in_pvp:
            f |= enums.PlayerFlags.IN_PVP
        if self.hide_helm:
            f |= enums.PlayerFlags.HIDE_HELM
        if self.hide_cloak:
            f |= enums.PlayerFlags.HIDE_CLOAK
        if self.has_partial_play_time:
            f |= enums.PlayerFlags.PARTIAL_PLAY_TIME
        if self.has_no_play_time:
            f |= enums.PlayerFlags.NO_PLAY_TIME
        if self.in_sanctuary:
            f |= enums.PlayerFlags.SANCTUARY
        if self.on_taxi_benchmark:
            f |= enums.PlayerFlags.TAXI_BENCHMARK
        if self.has_pvp_timer:
            f |= enums.PlayerFlags.PVP_TIMER

        return f

    def visible_item_fields(self, slot: enums.EquipmentSlot, item: Optional[Item]) -> Dict[enums.UpdateField, Any]:
        fields_start = enums.PlayerFields.VISIBLE_ITEM_START + (slot * 12)
        if item:
            enchantments = item.enchantment_map()
            fields = {}
            for ench_slot in enums.EnchantmentSlot:
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

    def inventory_fields(self, slot: enums.EquipmentSlot, item: Optional[Item]) -> Dict[enums.UpdateField, Any]:
        field = enums.PlayerFields.INVENTORY_START + (slot * 2)
        if item:
            return {field: item.guid}
        return {field: 0}

    @classmethod
    def New(
        cls,
        account: Account,
        realm: Realm,
        name: Text,
        race: constants.ChrRaces,
        class_: constants.ChrClasses,
        gender: enums.Gender,
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
        starting_location = game.StartingLocations.get(race=race.id)
        starting_items = game.StartingItems.get(race=race.id, class_=class_.id, gender=gender)

        team = enums.Team.ALLIANCE
        if race.id in (enums.EChrRaces.ORC, enums.EChrRaces.UNDEAD, enums.EChrRaces.TAUREN, enums.EChrRaces.TROLL):
            team = enums.Team.HORDE

        # Get starting stats.
        starting_stats = game.StartingStats.get(race=race, class_=class_)

        player = Player(
            account=account,
            realm=realm,
            name=name,
            level=kwargs.pop('level', 1),
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
            base_health=starting_stats.base_health,
            base_power=starting_stats.base_power,
            strength=starting_stats.strength,
            agility=starting_stats.agility,
            stamina=starting_stats.stamina,
            intellect=starting_stats.intellect,
            spirit=starting_stats.spirit,
            **kwargs,
        )

        for slot in range(enums.InventorySlots.EQUIPMENT_START, enums.InventorySlots.KEYRING_END):
            PlayerInventorySlot(
                player=player,
                slot=slot,
            )

        equipment = player.equipment()
        for equipment_dict in starting_items.equipment:
            slot = enums.EquipmentSlot[equipment_dict['equipment_slot']]
            equipment[slot].item = Item.New(game.ItemTemplate[equipment_dict['entry']])

        backpack = player.backpack()
        for i, entry in enumerate(starting_items.items):
            backpack[i].item = Item.New(game.ItemTemplate[entry])

        return player

    #
    # Class Methods (should be overwritten in children).
    #
    def type_id(self) -> enums.TypeID:
        return enums.TypeID.PLAYER

    def type_mask(self) -> enums.TypeMask:
        return super(Player, self).type_mask() | enums.TypeMask.PLAYER

    def high_guid(self) -> enums.HighGUID:
        return enums.HighGUID.PLAYER

    def num_fields(self) -> int:
        return 0x06 + 0xB6 + 0x446

    def calculate_attack_time(self, slot: enums.EquipmentSlot) -> int:
        equipment = self.equipment()

        base = 1000 if slot == enums.EquipmentSlot.MAIN_HAND else 0
        if equipment[slot].item:
            base = equipment[slot].item.base_item.delay

        return base

    def calculate_damage(self, slot: enums.EquipmentSlot) -> Tuple[float, float]:
        equipment = self.equipment()

        base = 1.0, 1.0
        if equipment[slot].item:
            base = equipment[slot].item.base_item.dmg(enums.SpellSchool.NORMAL)

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

    def calculate_resistance_buff(self, school: enums.SpellSchool) -> int:
        if school % 2 == 0:
            return int(-school - 1)
        return int(school + 1)

    def calculate_bonus_damage(self, school: enums.SpellSchool) -> int:
        if school % 2 == 0:
            return int(-school - 1)
        return int(school + 1)

    def calculate_bonus_damage_percent(self, school: enums.SpellSchool) -> float:
        return 1.0

    def calculate_melee_attack_power(self) -> int:
        return self.strength * 5

    def calculate_ranged_attack_power(self) -> int:
        return self.agility * 5

    def calculate_strength(self) -> int:
        return self.strength - 1

    def calculate_agility(self) -> int:
        return self.agility + 2

    def calculate_stamina(self) -> int:
        return self.stamina - 3

    def calculate_intellect(self) -> int:
        return self.intellect + 4

    def calculate_spirit(self) -> int:
        return self.spirit - 5

    def calculate_block_percent(self) -> float:
        return 10.0

    def calculate_dodge_percent(self) -> float:
        return 20.0

    def calculate_parry_percent(self) -> float:
        return 30.0

    def calculate_melee_crit_percent(self) -> float:
        return 15.0

    def calculate_ranged_crit_percent(self) -> float:
        return 25.0

    def bytes_4(self) -> int:
        b = 0
        if self.is_tracking_stealth:
            b |= enums.PlayerByteFlags.TRACK_STEALTHED
        if self.has_release_timer:
            b |= enums.PlayerByteFlags.RELEASE_TIMER
        if self.has_no_release_window:
            b |= enums.PlayerByteFlags.NO_RELEASE_WINDOW

        b |= (self.combo_points or 0) << 8

        # byte 3: action bars state? maybe sent by client
        # byte 4: highest rank info, probably unused

        return b

    def bytes_5(self) -> int:
        b = 0
        f = 0
        if self.can_detect_amore_0:
            f |= enums.PlayerByte2Flags.DETECT_AMORE_0
        if self.can_detect_amore_1:
            f |= enums.PlayerByte2Flags.DETECT_AMORE_1
        if self.can_detect_amore_2:
            f |= enums.PlayerByte2Flags.DETECT_AMORE_2
        if self.can_detect_amore_3:
            f |= enums.PlayerByte2Flags.DETECT_AMORE_3
        if self.in_stealth:
            f |= enums.PlayerByte2Flags.STEALTH
        if self.has_invisibility_glow:
            f |= enums.PlayerByte2Flags.INVISIBILITY_GLOW

        # byte 0: honor points
        b |= (f << 8)
        return b

    def get_ammo(self) -> int:
        return 12654  # TODO: actually find equipped ammo

    def update_fields(self) -> Dict[enums.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        f = enums.PlayerFields
        uf = enums.UnitFields
        fields: Dict[enums.UpdateField, Any] = defaultdict(lambda: 0)

        equipment = self.equipment()

        # Populate fields for virtual items (i.e. how sheathed items should
        # be displayed).
        if self.sheathed_state == enums.SheathedState.MELEE:
            if enums.EquipmentSlot.MAIN_HAND in equipment:
                fields.update(
                    self.virtual_item_fields(
                        enums.EquipmentSlot.MAIN_HAND,
                        equipment[enums.EquipmentSlot.MAIN_HAND].item.base_item,
                    ))

            if enums.EquipmentSlot.OFF_HAND in equipment:
                fields.update(
                    self.virtual_item_fields(
                        enums.EquipmentSlot.OFF_HAND,
                        equipment[enums.EquipmentSlot.OFF_HAND].item.base_item,
                    ))

        elif self.sheathed_state == enums.SheathedState.RANGED:
            if enums.EquipmentSlot.RANGED in equipment:
                fields.update(
                    self.virtual_item_fields(
                        enums.EquipmentSlot.RANGED,
                        equipment[enums.EquipmentSlot.RANGED].item.base_item,
                    ))

        # Populate equipment fields.
        for equipment_slot in enums.EquipmentSlot:
            slot = equipment[equipment_slot]
            if slot.item:
                fields.update(self.visible_item_fields(equipment_slot, slot.item))
                fields.update(self.inventory_fields(equipment_slot, slot.item))

        # Populate backpack fields.
        for slot in self.inventory:
            if slot.item:
                fields[f.INVENTORY_START + (slot.slot * 2)] = slot.item.guid
            else:
                fields[f.INVENTORY_START + (slot.slot * 2)] = game_object.GUID(0)

        fields.update({
            uf.BASEATTACKTIME: self.calculate_attack_time(enums.EquipmentSlot.MAIN_HAND),
            uf.OFFHANDATTACKTIME: self.calculate_attack_time(enums.EquipmentSlot.OFF_HAND),
            uf.RANGEDATTACKTIME: self.calculate_attack_time(enums.EquipmentSlot.RANGED),
            uf.MINDAMAGE: self.calculate_damage(enums.EquipmentSlot.MAIN_HAND)[0],
            uf.MAXDAMAGE: self.calculate_damage(enums.EquipmentSlot.MAIN_HAND)[1],
            uf.MINOFFHANDDAMAGE: self.calculate_damage(enums.EquipmentSlot.OFF_HAND)[0],
            uf.MAXOFFHANDDAMAGE: self.calculate_damage(enums.EquipmentSlot.OFF_HAND)[1],
            uf.MINRANGEDDAMAGE: self.calculate_damage(enums.EquipmentSlot.RANGED)[0],
            uf.MAXRANGEDDAMAGE: self.calculate_damage(enums.EquipmentSlot.RANGED)[1],
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
                f.GUILDRANK: self.guild_membership.rank.slot,
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
            f.PVP_MEDALS: 0,
            f.COMBAT_RATING_1: 0,
        })

        # Quest updates.
        for i, quest in enumerate(self.quests):
            start_field = f.QUEST_LOG_1_1 + (i * 3)
            fields.update({
                start_field + 0: quest.base_quest.id,
                start_field + 1: quest.flags(),
                start_field + 2: quest.due - int(time.time()) if quest.due else 0,
            })

        # Stat changes.
        if self.calculate_strength() - self.strength > 0:
            fields[f.POSSTAT0] = self.calculate_strength() - self.strength
        else:
            fields[f.NEGSTAT0] = self.calculate_strength() - self.strength

        if self.calculate_agility() - self.agility > 0:
            fields[f.POSSTAT1] = self.calculate_agility() - self.agility
        else:
            fields[f.NEGSTAT1] = self.calculate_agility() - self.agility

        if self.calculate_stamina() - self.stamina > 0:
            fields[f.POSSTAT2] = self.calculate_stamina() - self.stamina
        else:
            fields[f.NEGSTAT2] = self.calculate_stamina() - self.stamina

        if self.calculate_intellect() - self.intellect > 0:
            fields[f.POSSTAT3] = self.calculate_intellect() - self.intellect
        else:
            fields[f.NEGSTAT3] = self.calculate_intellect() - self.intellect

        if self.calculate_spirit() - self.spirit > 0:
            fields[f.POSSTAT4] = self.calculate_spirit() - self.spirit
        else:
            fields[f.NEGSTAT4] = self.calculate_spirit() - self.spirit

        # Resistance buffs.
        for school in enums.SpellSchool:
            buff = self.calculate_resistance_buff(school)
            if buff < 0:
                fields[f.RESISTANCEBUFFMODSNEGATIVE + school] = buff
            else:
                fields[f.RESISTANCEBUFFMODSPOSITIVE + school] = buff

            dmg = self.calculate_bonus_damage(school)
            if dmg < 0:
                fields[f.MOD_DAMAGE_DONE_NEG + school] = buff
            else:
                fields[f.MOD_DAMAGE_DONE_POS + school] = buff

            dmg_pct = self.calculate_bonus_damage_percent(school)
            fields[f.MOD_DAMAGE_DONE_PCT + school] = dmg_pct

        # Skills
        for skill in self.skills:
            base_field = f.SKILL_INFO_1_1 + (skill.skill.id * 3)

            fields.update({
                base_field + 0: skill.skill.id,  # upper 16 bits is "step"
                base_field + 1: skill.level | (skill.max_level() << 16),
                base_field + 2: skill.temp_bonus() | (skill.bonus << 16),
            })

        # 1 bit per zone
        for zone_id in range(enums.MAX_EXPLORED_ZONES):
            if zone_id in self.explored_zones:
                field = f.EXPLORED_ZONES_1 + (zone_id // 32)
                byte = 1 << (zone_id % 32)

                fields[field] = fields.get(field, 0) | byte

        fields.update({
            f.FLAGS: self.player_flags(),
            f.BYTES: self.skin_color | self.face << 8 | self.hair_style << 16 | self.hair_color << 24,
            f.BYTES_2: self.feature,
            f.BYTES_3: self.gender,
            f.COMBO_TARGET: self.combo_target.guid if self.combo_target else 0,
            f.XP: self.xp,
            f.NEXT_LEVEL_XP: enums.NextLevelXP(self.level),
            f.CHARACTER_POINTS1: self.level,  # TODO: talents
            f.CHARACTER_POINTS2: enums.MaxNumberOfProfessions(),  # TODO: professions are spells?
            f.BLOCK_PERCENTAGE: self.calculate_block_percent(),
            f.DODGE_PERCENTAGE: self.calculate_dodge_percent(),
            f.PARRY_PERCENTAGE: self.calculate_parry_percent(),
            f.CRIT_PERCENTAGE: self.calculate_melee_crit_percent(),
            f.RANGED_CRIT_PERCENTAGE: self.calculate_ranged_crit_percent(),
            f.REST_STATE_EXPERIENCE: self.rested_xp,
            f.COINAGE: self.money,
            f.BYTES_4: self.bytes_4(),
            f.AMMO_ID: self.get_ammo(),
            f.BYTES2: self.bytes_5(),
            f.WATCHED_FACTION_INDEX: self.watched_faction.reputation_index if self.watched_faction else -1,
            f.TRACK_CREATURES: 0,  # TODO: spells
            f.TRACK_RESOURCES: 0,  # TODO: spells
            f.SELF_RES_SPELL: 0,  # TODO: spell ID of self resurrecting spell
            f.FARSIGHT: 0,  # TODO: world objects
        })

        return {**super(Player, self).update_fields(), **fields}
