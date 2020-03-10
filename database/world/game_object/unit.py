from typing import Any, Dict, Optional, Tuple

from pony import orm

from database import constants
from database.dbc import constants as c
from database.dbc import item_template, unit_template
from database.world.game_object import game_object, item


class Unit(game_object.GameObject):
    level = orm.Required(int, min=1)
    race = orm.Required(c.Race)
    class_ = orm.Required(c.Class)
    gender = orm.Required(c.Gender)

    sheathed_state = orm.Required(c.SheathedState, default=c.SheathedState.UNARMED)
    stand_state = orm.Required(c.StandState, default=c.StandState.STAND)
    emote_state = orm.Optional(int)

    # Stats.
    strength = orm.Required(int, default=0)  # TODO: make this not have a default
    agility = orm.Required(int, default=0)  # TODO: make this not have a default
    stamina = orm.Required(int, default=0)  # TODO: make this not have a default
    intellect = orm.Required(int, default=0)  # TODO: make this not have a default
    spirit = orm.Required(int, default=0)  # TODO: make this not have a default

    # The current team.
    team = orm.Required(c.Team)

    # For NPC units, they will link to a template.
    base_unit = orm.Optional(unit_template.UnitTemplate)

    # For NPC units, they will have some equipment.
    # These aren't real items, just visible templates.
    npc_main_hand = orm.Optional(item_template.ItemTemplate, reverse='npc_main_hands')
    npc_off_hand = orm.Optional(item_template.ItemTemplate, reverse='npc_off_hands')
    npc_ranged = orm.Optional(item_template.ItemTemplate, reverse='npc_rangeds')

    auras = orm.Set('Aura')

    # Unit stats.
    base_health = orm.Required(int)
    base_power = orm.Required(int)

    health_percent = orm.Optional(float, min=0, max=1, default=1)
    power_percent = orm.Optional(float, min=0, max=1, default=1)

    # Flags.
    is_non_attackable = orm.Required(bool, default=False)
    has_movement_disabled = orm.Required(bool, default=False)
    is_pvp_attackable = orm.Required(bool, default=False)
    has_rename = orm.Required(bool, default=False)
    is_resting = orm.Required(bool, default=False)
    is_ooc_not_attackable = orm.Required(bool, default=False)
    is_passive = orm.Required(bool, default=False)
    is_pvp = orm.Required(bool, default=False)
    is_silenced = orm.Required(bool, default=False)
    is_pacified = orm.Required(bool, default=False)
    is_disable_rotate = orm.Required(bool, default=False)
    is_in_combat = orm.Required(bool, default=False)
    is_not_selectable = orm.Required(bool, default=False)
    is_skinnable = orm.Required(bool, default=False)
    is_auras_visible = orm.Required(bool, default=False)
    is_sheathe = orm.Required(bool, default=False)
    is_not_attackable_1 = orm.Required(bool, default=False)
    is_looting = orm.Required(bool, default=False)
    is_pet_in_combat = orm.Required(bool, default=False)
    is_stunned = orm.Required(bool, default=False)
    is_taxi_flight = orm.Required(bool, default=False)
    is_disarmed = orm.Required(bool, default=False)
    is_confused = orm.Required(bool, default=False)
    is_fleeing = orm.Required(bool, default=False)
    is_player_controlled = orm.Required(bool, default=False)

    is_always_stand = orm.Required(bool, default=False)
    is_creep = orm.Required(bool, default=False)
    is_untrackable = orm.Required(bool, default=False)

    is_lootable = orm.Required(bool, default=False)
    is_track_unit = orm.Required(bool, default=False)
    is_tapped = orm.Required(bool, default=False)
    is_rooted = orm.Required(bool, default=False)
    is_specialinfo = orm.Required(bool, default=False)

    # Relationships to other units.
    target = orm.Optional('Unit', reverse='targeted_by')
    targeted_by = orm.Set('Unit', reverse='target')
    control = orm.Optional('Unit', reverse='controller')
    controller = orm.Optional('Unit', reverse='control')
    summon = orm.Optional('Unit', reverse='summoner')
    summoner = orm.Optional('Unit', reverse='summon')
    created = orm.Set('Unit', reverse='created_by')
    created_by = orm.Optional('Unit', reverse='created')
    channeling = orm.Optional('Unit', reverse='channeled_by')
    channeled_by = orm.Set('Unit', reverse='channeling')
    mount = orm.Optional('Unit', reverse='mounted_by')
    mounted_by = orm.Optional('Unit', reverse='mount')

    # Unit location information.
    x = orm.Required(float)
    y = orm.Required(float)
    z = orm.Required(float)
    o = orm.Required(float)

    def position(self) -> Tuple[float, float, float]:
        """Get the current position of the object.

        All objects either have a position, or have a parent who has a 
        position, so a result from this should always be possible.

        Returns:
            A 3-tuple of floats (x, y, z).
        """
        return self.x, self.y, self.z

    #
    # Class Methods (should be overwritten in children).
    #
    def entry(self) -> Optional[int]:
        return self.base_unit.entry if self.base_unit else None

    def type_id(self) -> c.TypeID:
        return c.TypeID.UNIT

    def type_mask(self) -> c.TypeMask:
        return super(Unit, self).type_mask() | c.TypeMask.UNIT

    def update_flags(self) -> c.UpdateFlags:
        return c.UpdateFlags.ALL | c.UpdateFlags.LIVING | c.UpdateFlags.HAS_POSITION

    def high_guid(self) -> c.HighGUID:
        return c.HighGUID.UNIT

    def num_fields(self) -> int:
        return 0x06 + 0xB6

    def bytes_0(self) -> int:
        return self.race | self.class_ << 8 | self.gender << 16

    def bytes_1(self) -> int:
        f = 0
        if self.is_always_stand:
            f |= c.UnitBytes1Flags.ALWAYS_STAND
        if self.is_creep:
            f |= c.UnitBytes1Flags.CREEP
        if self.is_untrackable:
            f |= c.UnitBytes1Flags.UNTRACKABLE

        return self.stand_state | f << 16

    def bytes_2(self) -> int:
        return self.sheathed_state

    def flags(self) -> c.UnitFlags:
        f = c.UnitFlags.NONE
        if self.is_non_attackable:
            f |= c.UnitFlags.NON_ATTACKABLE
        if self.has_movement_disabled:
            f |= c.UnitFlags.DISABLE_MOVE
        if self.is_pvp_attackable:
            f |= c.UnitFlags.PVP_ATTACKABLE
        if self.has_rename:
            f |= c.UnitFlags.RENAME
        if self.is_resting:
            f |= c.UnitFlags.RESTING
        if self.is_ooc_not_attackable:
            f |= c.UnitFlags.OOC_NOT_ATTACKABLE
        if self.is_passive:
            f |= c.UnitFlags.PASSIVE
        if self.is_pvp:
            f |= c.UnitFlags.PVP
        if self.is_silenced:
            f |= c.UnitFlags.SILENCED
        if self.is_pacified:
            f |= c.UnitFlags.PACIFIED
        if self.is_disable_rotate:
            f |= c.UnitFlags.DISABLE_ROTATE
        if self.is_in_combat:
            f |= c.UnitFlags.IN_COMBAT
        if self.is_not_selectable:
            f |= c.UnitFlags.NOT_SELECTABLE
        if self.is_skinnable:
            f |= c.UnitFlags.SKINNABLE
        if self.is_auras_visible:
            f |= c.UnitFlags.AURAS_VISIBLE
        if self.is_sheathe:
            f |= c.UnitFlags.SHEATHE
        if self.is_not_attackable_1:
            f |= c.UnitFlags.NOT_ATTACKABLE_1
        if self.is_looting:
            f |= c.UnitFlags.LOOTING
        if self.is_pet_in_combat:
            f |= c.UnitFlags.PET_IN_COMBAT
        if self.is_stunned:
            f |= c.UnitFlags.STUNNED
        if self.is_taxi_flight:
            f |= c.UnitFlags.TAXI_FLIGHT
        if self.is_disarmed:
            f |= c.UnitFlags.DISARMED
        if self.is_confused:
            f |= c.UnitFlags.CONFUSED
        if self.is_fleeing:
            f |= c.UnitFlags.FLEEING
        if self.is_player_controlled:
            f |= c.UnitFlags.PLAYER_CONTROLLED

        return f

    def dynamic_flags(self) -> c.UnitDynamicFlags:
        f = c.UnitDynamicFlags.NONE

        if self.is_lootable:
            f |= c.UnitDynamicFlags.LOOTABLE
        if self.is_track_unit:
            f |= c.UnitDynamicFlags.TRACK_UNIT
        if self.is_tapped:
            f |= c.UnitDynamicFlags.TAPPED
        if self.is_rooted:
            f |= c.UnitDynamicFlags.ROOTED
        if self.is_specialinfo:
            f |= c.UnitDynamicFlags.SPECIALINFO
        if self.health_percent == 0:
            f |= c.UnitDynamicFlags.DEAD

        return f

    def calculate_cast_speed_mod(self) -> float:
        return 1.0

    def display_id(self) -> int:
        if self.base_unit:
            return self.base_unit.ModelId1

        # For players, read from the DBC.
        race_info = constants.ChrRaces[self.race]
        if self.gender == c.Gender.MALE:
            return race_info.male_display_id
        return race_info.female_display_id

    def faction_template(self) -> int:
        if self.base_unit:
            if self.team == c.Team.ALLIANCE:
                return self.base_unit.FactionAlliance
            return self.base_unit.FactionHorde

        return constants.ChrRaces[self.race].faction_template_id

    def health(self) -> int:
        return self.max_health() * self.health_percent

    def max_health(self) -> int:
        return self.base_health

    def power(self) -> int:
        return self.max_power() * self.power_percent

    def max_power(self) -> int:
        return self.base_power

    def power_type(self) -> c.PowerType:
        # TODO: use ChrClasses for this information
        if self.class_ == c.Class.WARRIOR:
            return c.PowerType.RAGE
        elif self.class_ == c.Class.ROGUE:
            return c.PowerType.ENERGY
        return c.PowerType.MANA

    def virtual_item_fields(self, slot: c.EquipmentSlot,
                            item: Optional[item_template.ItemTemplate]) -> Dict[c.UpdateField, Any]:
        if not item:
            return {}

        if slot == c.EquipmentSlot.MAIN_HAND:
            DISPLAY = c.UnitFields.MAIN_HAND_DISPLAY
            INFO_0 = c.UnitFields.MAIN_HAND_INFO_0
            INFO_1 = c.UnitFields.MAIN_HAND_INFO_1
        elif slot == c.EquipmentSlot.OFF_HAND:
            DISPLAY = c.UnitFields.OFF_HAND_DISPLAY
            INFO_0 = c.UnitFields.OFF_HAND_INFO_0
            INFO_1 = c.UnitFields.OFF_HAND_INFO_1
        elif slot == c.EquipmentSlot.RANGED:
            DISPLAY = c.UnitFields.RANGED_DISPLAY
            INFO_0 = c.UnitFields.RANGED_INFO_0
            INFO_1 = c.UnitFields.RANGED_INFO_1
        else:
            return {}

        return {
            DISPLAY: item.displayid,
            INFO_0: (item.class_ | item.subclass << 8 | item.Material << 16 | item.InventoryType << 24),
            INFO_1: item.sheath,
        }

    def melee_attack_power_modifier(self) -> int:
        return 0

    def melee_attack_power_multiplier(self) -> float:
        return 1.0

    def ranged_attack_power_modifier(self) -> int:
        return 0

    def ranged_attack_power_multiplier(self) -> float:
        return 1.0

    def power_cost_modifier_field(self) -> Dict[c.UpdateField, Any]:
        modifier = 0
        return {
            c.UnitFields.POWER_COST_MODIFIER + self.power_type(): modifier,
        }

    def power_cost_multiplier_field(self) -> Dict[c.UpdateField, Any]:
        multiplier = 1.0
        return {
            c.UnitFields.POWER_COST_MULTIPLIER + self.power_type(): multiplier,
        }

    def calculate_strength(self) -> int:
        return self.strength

    def calculate_agility(self) -> int:
        return self.agility

    def calculate_stamina(self) -> int:
        return self.stamina

    def calculate_intellect(self) -> int:
        return self.intellect

    def calculate_spirit(self) -> int:
        return self.spirit

    def update_fields(self) -> Dict[c.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        f = c.UnitFields
        fields: Dict[c.UpdateField, Any] = {}

        if self.base_unit:
            # TODO: get data about virtual items for units
            fields.update(self.virtual_item_fields(c.EquipmentSlot.MAIN_HAND, self.npc_main_hand))
            fields.update(self.virtual_item_fields(c.EquipmentSlot.OFF_HAND, self.npc_off_hand))
            fields.update(self.virtual_item_fields(c.EquipmentSlot.RANGED, self.npc_ranged))

            fields.update({
                f.BASEATTACKTIME: self.base_unit.MeleeBaseAttackTime,
                f.OFFHANDATTACKTIME: self.base_unit.MeleeBaseAttackTime,
                f.RANGEDATTACKTIME: self.base_unit.RangedBaseAttackTime,
                f.MINDAMAGE: self.base_unit.MinMeleeDmg,
                f.MAXDAMAGE: self.base_unit.MaxMeleeDmg,
                f.MINOFFHANDDAMAGE: self.base_unit.MinMeleeDmg,
                f.MAXOFFHANDDAMAGE: self.base_unit.MaxMeleeDmg,
                f.MINRANGEDDAMAGE: self.base_unit.MinRangedDmg,
                f.MAXRANGEDDAMAGE: self.base_unit.MaxRangedDmg,
                f.NPC_FLAGS: self.base_unit.NpcFlags,
                f.ARMOR: self.base_unit.Armor,
                f.HOLY_RESISTANCE: self.base_unit.ResistanceHoly,
                f.FIRE_RESISTANCE: self.base_unit.ResistanceFire,
                f.NATURE_RESISTANCE: self.base_unit.ResistanceNature,
                f.FROST_RESISTANCE: self.base_unit.ResistanceFrost,
                f.SHADOW_RESISTANCE: self.base_unit.ResistanceShadow,
                f.ARCANE_RESISTANCE: self.base_unit.ResistanceArcane,
                f.ATTACK_POWER: self.base_unit.MeleeAttackPower,
                f.RANGED_ATTACK_POWER: self.base_unit.RangedAttackPower,
                f.COMBATREACH: 1.0,  # TODO: ObjectScale * ModelInfo.combat_reach
            })

        aura_flags = [0] * 48  # 6 fields => 24 bytes => 48 nibbles, one per aura
        aura_levels = [0] * 48  # 12 fields => 48 bytes, one per aura
        aura_applications = [0] * 48  # 12 fields => 48 bytes, one per aura
        aura_state = c.AuraState.NONE
        for aura in self.auras:
            aura_flags[aura.slot] = 0x09
            aura_levels[aura.slot] = 1  # TODO: aura caster levels?
            aura_applications[aura.slot] = 255 - 1  # TODO: aura stack count?
            aura_state |= aura.base_spell.aura_state_modifier

            fields[f.AURA + aura.slot] = aura.base_spell.id

        # aura_flags is a list of nibbles, convert it to a list of fields.
        # First, merge each nibble together to get a list of 24 bytes.
        aura_flags_fields = [0] * 6
        for i, aura_flag in enumerate(aura_flags):
            field = i // 8
            byte = i % 8
            aura_flags_fields[field] |= (aura_flag << (byte * 4))

        fields.update({f.AURAFLAGS + i: val for i, val in enumerate(aura_flags_fields)})

        # aura_levels is a list of bytes, each of which is part of a field.
        aura_levels_fields = [0] * 12
        for i, aura_level in enumerate(aura_levels):
            field = i // 4
            byte = i % 4
            aura_levels_fields[field] |= (aura_level << (byte * 8))

        fields.update({f.AURALEVELS + i: val for i, val in enumerate(aura_levels_fields)})

        # aura_applications is a list of bytes, each of which is part of a field.
        aura_applications_fields = [0] * 12
        for i, aura_application in enumerate(aura_applications):
            field = i // 4
            byte = i % 4
            aura_applications_fields[field] |= (aura_application << (byte * 8))

        fields.update({f.AURALEVELS + i: val for i, val in enumerate(aura_applications_fields)})

        # AURASTATE is a set of flags (just a single byte).
        fields[f.AURASTATE] = aura_state

        fields.update({
            f.CHARM: self.control.guid if self.control else None,
            f.SUMMON: self.summon.guid if self.summon else None,
            f.CHARMEDBY: self.controller.guid if self.controller else None,
            f.SUMMONEDBY: self.summoner.guid if self.summoner else None,
            f.CREATEDBY: self.created_by.guid if self.created_by else None,
            f.TARGET: self.target.guid if self.target else None,
            f.PERSUADED: self.created_by.guid if self.created_by else None,
            f.CHANNEL: self.channeling.guid if self.channeling else None,
            f.HEALTH: self.health(),
            f.POWER_START + self.power_type(): self.power(),
            f.MAXHEALTH: self.max_health(),
            f.MAX_POWER_START + self.power_type(): self.max_power(),
            f.LEVEL: self.level,
            f.FACTIONTEMPLATE: self.faction_template(),
            f.BYTES_0: self.bytes_0(),
            f.FLAGS: self.flags(),
            f.BOUNDINGRADIUS: 1.0,  # TODO: ObjectScale * ModelInfo.bounding_radius
            f.DISPLAYID: self.display_id(),
            f.NATIVEDISPLAYID: self.display_id(),
            f.MOUNTDISPLAYID: self.mount.display_id() if self.mount else 0,
            f.BYTES_1: self.bytes_1(),
            f.DYNAMIC_FLAGS: self.dynamic_flags(),
            f.CHANNEL_SPELL: 0,  # TODO: spell ID of the spell being channelled
            f.MOD_CAST_SPEED: self.calculate_cast_speed_mod(),
            f.CREATED_BY_SPELL: 0,  # TODO: spell ID of the spell which created this unit
            f.NPC_EMOTESTATE: self.emote_state,
            f.STRENGTH: self.calculate_strength(),
            f.AGILITY: self.calculate_agility(),
            f.STAMINA: self.calculate_stamina(),
            f.INTELLECT: self.calculate_intellect(),
            f.SPIRIT: self.calculate_spirit(),
            f.BASE_MANA: self.base_power,
            f.BASE_HEALTH: self.base_health,
            f.BYTES_2: self.bytes_2(),
            f.ATTACK_POWER_MODS: self.melee_attack_power_modifier(),
            f.ATTACK_POWER_MULTIPLIER: self.melee_attack_power_multiplier(),
            f.RANGED_ATTACK_POWER_MODS: self.ranged_attack_power_modifier(),
            f.RANGED_ATTACK_POWER_MULTIPLIER: self.ranged_attack_power_multiplier(),
        })

        fields.update(self.power_cost_modifier_field())
        fields.update(self.power_cost_multiplier_field())

        return {**super(Unit, self).update_fields(), **fields}
