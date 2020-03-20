from typing import Any, Dict, Optional, Tuple

from pony import orm

from database import constants, enums, game

from . import game_object


class Unit(game_object.GameObject):
    name = orm.Optional(str)
    level = orm.Required(int, min=1)
    race = orm.Required(constants.ChrRaces)
    class_ = orm.Required(constants.ChrClasses)
    gender = orm.Required(enums.Gender)

    sheathed_state = orm.Required(enums.SheathedState, default=enums.SheathedState.UNARMED)
    stand_state = orm.Required(enums.StandState, default=enums.StandState.STAND)
    emote_state = orm.Optional(int)

    # Stats.
    strength = orm.Required(int, default=0)
    agility = orm.Required(int, default=0)
    stamina = orm.Required(int, default=0)
    intellect = orm.Required(int, default=0)
    spirit = orm.Required(int, default=0)

    # The current team.
    team = orm.Required(enums.Team)

    # For NPC units, they will link to a template.
    base_unit = orm.Optional(game.UnitTemplate)

    # For NPC units, they will have some equipment.
    # These aren't real items, just visible templates.
    npc_main_hand = orm.Optional(game.ItemTemplate, reverse='npc_main_hands_backlink')
    npc_off_hand = orm.Optional(game.ItemTemplate, reverse='npc_off_hands_backlink')
    npc_ranged = orm.Optional(game.ItemTemplate, reverse='npc_rangeds_backlink')

    auras = orm.Set('Aura', reverse='applied_to')
    applied_auras = orm.Set('Aura', reverse='applied_by')

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
    created_by_spell = orm.Optional('Spell', reverse='unit_created_by_backlink')
    channeling_spell = orm.Optional('Spell', reverse='unit_channeling_backlink')

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

    def type_id(self) -> enums.TypeID:
        return enums.TypeID.UNIT

    def type_mask(self) -> enums.TypeMask:
        return super(Unit, self).type_mask() | enums.TypeMask.UNIT

    def update_flags(self) -> enums.UpdateFlags:
        return enums.UpdateFlags.ALL | enums.UpdateFlags.LIVING | enums.UpdateFlags.HAS_POSITION

    def high_guid(self) -> enums.HighGUID:
        return enums.HighGUID.UNIT

    def num_fields(self) -> int:
        return 0x06 + 0xB6

    def bytes_0(self) -> int:
        return self.race.id | self.class_.id << 8 | self.gender << 16

    def bytes_1(self) -> int:
        f = 0
        if self.is_always_stand:
            f |= enums.UnitBytes1Flags.ALWAYS_STAND
        if self.is_creep:
            f |= enums.UnitBytes1Flags.CREEP
        if self.is_untrackable:
            f |= enums.UnitBytes1Flags.UNTRACKABLE

        return self.stand_state | f << 16

    def bytes_2(self) -> int:
        return self.sheathed_state

    def flags(self) -> enums.UnitFlags:
        f = enums.UnitFlags.NONE
        if self.is_non_attackable:
            f |= enums.UnitFlags.NON_ATTACKABLE
        if self.has_movement_disabled:
            f |= enums.UnitFlags.DISABLE_MOVE
        if self.is_pvp_attackable:
            f |= enums.UnitFlags.PVP_ATTACKABLE
        if self.has_rename:
            f |= enums.UnitFlags.RENAME
        if self.is_resting:
            f |= enums.UnitFlags.RESTING
        if self.is_ooc_not_attackable:
            f |= enums.UnitFlags.OOC_NOT_ATTACKABLE
        if self.is_passive:
            f |= enums.UnitFlags.PASSIVE
        if self.is_pvp:
            f |= enums.UnitFlags.PVP
        if self.is_silenced:
            f |= enums.UnitFlags.SILENCED
        if self.is_pacified:
            f |= enums.UnitFlags.PACIFIED
        if self.is_disable_rotate:
            f |= enums.UnitFlags.DISABLE_ROTATE
        if self.is_in_combat:
            f |= enums.UnitFlags.IN_COMBAT
        if self.is_not_selectable:
            f |= enums.UnitFlags.NOT_SELECTABLE
        if self.is_skinnable:
            f |= enums.UnitFlags.SKINNABLE
        if self.is_auras_visible:
            f |= enums.UnitFlags.AURAS_VISIBLE
        if self.is_sheathe:
            f |= enums.UnitFlags.SHEATHE
        if self.is_not_attackable_1:
            f |= enums.UnitFlags.NOT_ATTACKABLE_1
        if self.is_looting:
            f |= enums.UnitFlags.LOOTING
        if self.is_pet_in_combat:
            f |= enums.UnitFlags.PET_IN_COMBAT
        if self.is_stunned:
            f |= enums.UnitFlags.STUNNED
        if self.is_taxi_flight:
            f |= enums.UnitFlags.TAXI_FLIGHT
        if self.is_disarmed:
            f |= enums.UnitFlags.DISARMED
        if self.is_confused:
            f |= enums.UnitFlags.CONFUSED
        if self.is_fleeing:
            f |= enums.UnitFlags.FLEEING
        if self.is_player_controlled:
            f |= enums.UnitFlags.PLAYER_CONTROLLED

        return f

    def dynamic_flags(self) -> enums.UnitDynamicFlags:
        f = enums.UnitDynamicFlags.NONE

        if self.is_lootable:
            f |= enums.UnitDynamicFlags.LOOTABLE
        if self.is_track_unit:
            f |= enums.UnitDynamicFlags.TRACK_UNIT
        if self.is_tapped:
            f |= enums.UnitDynamicFlags.TAPPED
        if self.is_rooted:
            f |= enums.UnitDynamicFlags.ROOTED
        if self.is_specialinfo:
            f |= enums.UnitDynamicFlags.SPECIALINFO
        if self.health_percent == 0:
            f |= enums.UnitDynamicFlags.DEAD

        return f

    def calculate_cast_speed_mod(self) -> float:
        return 1.0

    def display_info(self) -> game.UnitModelInfo:
        if self.base_unit:
            return self.base_unit.ModelId1

        if self.gender == enums.Gender.MALE:
            return self.race.male_display_info
        return self.race.female_display_info

    def faction_template(self) -> int:
        if self.base_unit:
            if self.team == enums.Team.ALLIANCE:
                return self.base_unit.FactionAlliance
            return self.base_unit.FactionHorde

        return self.race.faction.id

    def health(self) -> int:
        return self.max_health() * self.health_percent

    def max_health(self) -> int:
        return self.base_health

    def power(self) -> int:
        return self.max_power() * self.power_percent

    def max_power(self) -> int:
        return self.base_power

    def power_type(self) -> enums.PowerType:
        return self.class_.display_power

    def virtual_item_fields(self, slot: enums.EquipmentSlot,
                            item: Optional[game.ItemTemplate]) -> Dict[enums.UpdateField, Any]:
        if not item:
            return {}

        if slot == enums.EquipmentSlot.MAIN_HAND:
            DISPLAY = enums.UnitFields.MAIN_HAND_DISPLAY
            INFO_0 = enums.UnitFields.MAIN_HAND_INFO_0
            INFO_1 = enums.UnitFields.MAIN_HAND_INFO_1
        elif slot == enums.EquipmentSlot.OFF_HAND:
            DISPLAY = enums.UnitFields.OFF_HAND_DISPLAY
            INFO_0 = enums.UnitFields.OFF_HAND_INFO_0
            INFO_1 = enums.UnitFields.OFF_HAND_INFO_1
        elif slot == enums.EquipmentSlot.RANGED:
            DISPLAY = enums.UnitFields.RANGED_DISPLAY
            INFO_0 = enums.UnitFields.RANGED_INFO_0
            INFO_1 = enums.UnitFields.RANGED_INFO_1
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

    def power_cost_modifier_field(self) -> Dict[enums.UpdateField, Any]:
        modifier = 0
        return {
            enums.UnitFields.POWER_COST_MODIFIER + self.power_type(): modifier,
        }

    def power_cost_multiplier_field(self) -> Dict[enums.UpdateField, Any]:
        multiplier = 1.0
        return {
            enums.UnitFields.POWER_COST_MULTIPLIER + self.power_type(): multiplier,
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

    def update_fields(self) -> Dict[enums.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        f = enums.UnitFields
        fields: Dict[enums.UpdateField, Any] = {}

        if self.base_unit:
            # TODO: get data about virtual items for units
            fields.update(self.virtual_item_fields(enums.EquipmentSlot.MAIN_HAND, self.npc_main_hand))
            fields.update(self.virtual_item_fields(enums.EquipmentSlot.OFF_HAND, self.npc_off_hand))
            fields.update(self.virtual_item_fields(enums.EquipmentSlot.RANGED, self.npc_ranged))

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
            })

        model_info = self.display_info()
        fields.update({
            f.COMBATREACH: self.scale * model_info.combat_reach,
            f.BOUNDINGRADIUS: self.scale * model_info.bounding_radius,
        })

        aura_flags = [0] * 48  # 6 fields => 24 bytes => 48 nibbles, one per aura
        aura_levels = [0] * 48  # 12 fields => 48 bytes, one per aura
        aura_applications = [0] * 48  # 12 fields => 48 bytes, one per aura
        aura_state = enums.AuraState.NONE
        for aura in self.auras:
            aura_flags[aura.slot] = 0x09
            aura_levels[aura.slot] = aura.applied_by.level
            aura_applications[aura.slot] = aura.applications - 1
            aura_state |= aura.base_spell.target_aura_state

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
            f.DISPLAYID: self.display_info().id,
            f.NATIVEDISPLAYID: self.display_info().id,
            f.MOUNTDISPLAYID: self.mount.display_info().id if self.mount else 0,
            f.BYTES_1: self.bytes_1(),
            f.DYNAMIC_FLAGS: self.dynamic_flags(),
            f.CHANNEL_SPELL: self.channeling_spell.id if self.channeling_spell else 0,
            f.MOD_CAST_SPEED: self.calculate_cast_speed_mod(),
            f.CREATED_BY_SPELL: self.created_by_spell.id if self.created_by_spell else 0,
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
