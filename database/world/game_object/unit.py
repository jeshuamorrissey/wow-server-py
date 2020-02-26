from typing import Any, Dict, Tuple, Optional

from pony import orm

from database.dbc import chr_races
from database.dbc import constants as c
from database.world.game_object import game_object
from database.dbc import unit_template
from database.world.game_object import item


class Unit(game_object.GameObject):
    level = orm.Required(int, min=1)
    race = orm.Required(c.Race)
    class_ = orm.Required(c.Class)
    gender = orm.Required(c.Gender)

    sheathed_state = orm.Required(c.SheathedState,
                                  default=c.SheathedState.UNARMED)

    # The current team.
    team = orm.Required(c.Team)

    # For NPC units, they will link to a template.
    base_unit = orm.Optional(unit_template.UnitTemplate)

    # Unit statistics.
    base_health = orm.Required(int)
    base_power = orm.Required(int)

    health_percent = orm.Optional(float, min=0, max=1, default=1)
    power_percent = orm.Optional(float, min=0, max=1, default=1)

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

    def bytes_2(self) -> int:
        return self.sheathed_state

    def display_id(self) -> int:
        if self.base_unit:
            return self.base_unit.ModelId1

        # For players, read from the DBC.
        race_info = chr_races.ChrRaces[self.race]
        if self.gender == c.Gender.MALE:
            return race_info.male_display_id
        return race_info.female_display_id

    def faction_template(self) -> int:
        if self.base_unit:
            if self.team == c.Team.ALLIANCE:
                return self.base_unit.FactionAlliance
            return self.base_unit.FactionHorde

        return chr_races.ChrRaces[self.race].faction_template_id

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

    def virtual_item_fields(
            self, slot: c.EquipmentSlot,
            item: Optional[item.Item]) -> Dict[c.UpdateField, Any]:
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

        i = item.base_item
        info_0 = (i.class_ | i.subclass << 8 | i.Material << 16
                  | i.InventoryType << 24)
        return {
            DISPLAY: i.displayid,
            INFO_0: info_0,
            INFO_1: i.sheath,
        }

    def update_fields(self) -> Dict[c.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        f = c.UnitFields
        fields: Dict[c.UpdateField, Any] = {}

        if self.base_unit:
            # TODO: get data about virtual items for units
            fields.update({
                f.MAIN_HAND_DISPLAY: 0,
                f.OFF_HAND_DISPLAY: 0,
                f.RANGED_DISPLAY: 0,
                f.MAIN_HAND_INFO_0: 0,
                f.MAIN_HAND_INFO_1: 0,
                f.OFF_HAND_INFO_0: 0,
                f.OFF_HAND_INFO_1: 0,
                f.RANGED_INFO_0: 0,
                f.RANGED_INFO_1: 0,
            })

        fields.update({
            f.CHARM:
            self.control.guid if self.control else None,
            f.SUMMON:
            self.summon.guid if self.summon else None,
            f.CHARMEDBY:
            self.controller.guid if self.controller else None,
            f.SUMMONEDBY:
            self.summoner.guid if self.summoner else None,
            f.CREATEDBY:
            self.created_by.guid if self.created_by else None,
            f.TARGET:
            self.target.guid if self.target else None,
            f.PERSUADED:
            self.created_by.guid if self.created_by else None,
            f.CHANNEL:
            self.channeling.guid if self.channeling else None,
            f.HEALTH:
            self.health(),
            f.POWER_START + self.power_type():
            self.power(),
            f.MAXHEALTH:
            self.max_health(),
            f.MAX_POWER_START + self.power_type():
            self.max_power(),
            f.LEVEL:
            self.level,
            f.FACTIONTEMPLATE:
            self.faction_template(),
            f.BYTES_0:
            self.bytes_0(),
            f.FLAGS:
            0,
            f.AURA:
            0,
            f.AURA_LAST:
            0,
            f.AURAFLAGS:
            0,
            f.AURAFLAGS_01:
            0,
            f.AURAFLAGS_02:
            0,
            f.AURAFLAGS_03:
            0,
            f.AURAFLAGS_04:
            0,
            f.AURAFLAGS_05:
            0,
            f.AURALEVELS:
            0,
            f.AURALEVELS_LAST:
            0,
            f.AURAAPPLICATIONS:
            0,
            f.AURAAPPLICATIONS_LAST:
            0,
            f.AURASTATE:
            0,
            f.BASEATTACKTIME:
            1000,
            f.OFFHANDATTACKTIME:
            1000,
            f.RANGEDATTACKTIME:
            1000,
            f.BOUNDINGRADIUS:
            1.0,
            f.COMBATREACH:
            1.0,
            f.DISPLAYID:
            self.display_id(),
            f.NATIVEDISPLAYID:
            self.display_id(),
            f.MOUNTDISPLAYID:
            0,
            f.MINDAMAGE:
            10.0,
            f.MAXDAMAGE:
            20.0,
            f.MINOFFHANDDAMAGE:
            10.0,
            f.MAXOFFHANDDAMAGE:
            20.0,
            f.BYTES_1:
            0,
            f.DYNAMIC_FLAGS:
            0,
            f.CHANNEL_SPELL:
            0,
            f.MOD_CAST_SPEED:
            0,
            f.CREATED_BY_SPELL:
            0,
            f.NPC_FLAGS:
            0,
            f.NPC_EMOTESTATE:
            0,
            f.TRAINING_POINTS:
            0,
            f.STAT0:
            1,
            f.STAT1:
            2,
            f.STAT2:
            3,
            f.STAT3:
            4,
            f.STAT4:
            5,
            f.RESISTANCES:
            1,
            f.RESISTANCES_01:
            2,
            f.RESISTANCES_02:
            3,
            f.RESISTANCES_03:
            4,
            f.RESISTANCES_04:
            5,
            f.RESISTANCES_05:
            6,
            f.RESISTANCES_06:
            7,
            f.BASE_MANA:
            self.base_power,
            f.BASE_HEALTH:
            self.base_health,
            f.BYTES_2:
            self.bytes_2(),
            f.ATTACK_POWER:
            10,
            f.ATTACK_POWER_MODS:
            1,
            f.ATTACK_POWER_MULTIPLIER:
            2.0,
            f.RANGED_ATTACK_POWER:
            10,
            f.RANGED_ATTACK_POWER_MODS:
            1,
            f.RANGED_ATTACK_POWER_MULTIPLIER:
            2.0,
            f.MINRANGEDDAMAGE:
            10.0,
            f.MAXRANGEDDAMAGE:
            10.0,
            f.POWER_COST_MODIFIER:
            0,
            f.POWER_COST_MODIFIER_01:
            0,
            f.POWER_COST_MODIFIER_02:
            0,
            f.POWER_COST_MODIFIER_03:
            0,
            f.POWER_COST_MODIFIER_04:
            0,
            f.POWER_COST_MODIFIER_05:
            0,
            f.POWER_COST_MODIFIER_06:
            0,
            f.POWER_COST_MULTIPLIER:
            0,
            f.POWER_COST_MULTIPLIER_01:
            0,
            f.POWER_COST_MULTIPLIER_02:
            0,
            f.POWER_COST_MULTIPLIER_03:
            0,
            f.POWER_COST_MULTIPLIER_04:
            0,
            f.POWER_COST_MULTIPLIER_05:
            0,
            f.POWER_COST_MULTIPLIER_06:
            0,
            f.PADDING:
            0,
        })

        return {**super(Unit, self).update_fields(), **fields}
