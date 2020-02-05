from typing import Tuple, Dict, Any

from pony import orm

from database.dbc import constants as c
from database.world.game_object.game_object import GameObject


class Unit(GameObject):
    level = orm.Required(int, min=1)
    race = orm.Required(c.Race)
    class_ = orm.Required(c.Class)
    gender = orm.Required(c.Gender)

    # For NPC units, they will link to a template.
    base_unit = orm.Optional('UnitTemplate')

    # For pets, they will have a master.
    master = orm.Optional('Player')

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
    def type_id(self) -> c.TypeID:
        return c.TypeID.UNIT

    def type_mask(self) -> c.TypeMask:
        return super(Unit, self).type_mask() | c.TypeMask.UNIT

    def update_flags(self) -> c.UpdateFlags:
        return c.UpdateFlags.ALL | c.UpdateFlags.LIVING | c.UpdateFlags.HAS_POSITION

    def high_guid(self) -> c.HighGUID:
        if self.master:
            return c.HighGUID.PET
        return c.HighGUID.UNIT

    def num_fields(self) -> int:
        return 0x06 + 0xB6

    def update_fields(self) -> Dict[c.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        f = c.UnitFields
        fields = {
            f.CHARM: 0,
            f.SUMMON: 0,
            f.CHARMEDBY: 0,
            f.SUMMONEDBY: 0,
            f.CREATEDBY: 0,
            f.TARGET: 0,
            f.PERSUADED: 0,
            f.CHANNEL_OBJECT: 0,
            f.HEALTH: 0,
            f.POWER1: 0,
            f.POWER2: 0,
            f.POWER3: 0,
            f.POWER4: 0,
            f.POWER5: 0,
            f.MAXHEALTH: 0,
            f.MAXPOWER1: 0,
            f.MAXPOWER2: 0,
            f.MAXPOWER3: 0,
            f.MAXPOWER4: 0,
            f.MAXPOWER5: 0,
            f.LEVEL: 0,
            f.FACTIONTEMPLATE: 4,
            f.BYTES_0:
            self.race | self.class_ << 8 | self.gender << 16,  # MUST BE SET
            f.VIRTUAL_ITEM_SLOT_DISPLAY: 0,
            f.VIRTUAL_ITEM_SLOT_DISPLAY_01: 0,
            f.VIRTUAL_ITEM_SLOT_DISPLAY_02: 0,
            f.VIRTUAL_ITEM_INFO: 0,
            f.VIRTUAL_ITEM_INFO_01: 0,
            f.VIRTUAL_ITEM_INFO_02: 0,
            f.VIRTUAL_ITEM_INFO_03: 0,
            f.VIRTUAL_ITEM_INFO_04: 0,
            f.VIRTUAL_ITEM_INFO_05: 0,
            f.FLAGS: 0,
            f.AURA: 0,
            f.AURA_LAST: 0,
            f.AURAFLAGS: 0,
            f.AURAFLAGS_01: 0,
            f.AURAFLAGS_02: 0,
            f.AURAFLAGS_03: 0,
            f.AURAFLAGS_04: 0,
            f.AURAFLAGS_05: 0,
            f.AURALEVELS: 0,
            f.AURALEVELS_LAST: 0,
            f.AURAAPPLICATIONS: 0,
            f.AURAAPPLICATIONS_LAST: 0,
            f.AURASTATE: 0,
            f.BASEATTACKTIME: 0,
            f.OFFHANDATTACKTIME: 0,
            f.RANGEDATTACKTIME: 0,
            f.BOUNDINGRADIUS: 0,
            f.COMBATREACH: 0,
            f.DISPLAYID: 0,
            f.NATIVEDISPLAYID: 0,
            f.MOUNTDISPLAYID: 0,
            f.MINDAMAGE: 0,
            f.MAXDAMAGE: 0,
            f.MINOFFHANDDAMAGE: 0,
            f.MAXOFFHANDDAMAGE: 0,
            f.BYTES_1: 0,
            f.PETNUMBER: 0,
            f.PET_NAME_TIMESTAMP: 0,
            f.PETEXPERIENCE: 0,
            f.PETNEXTLEVELEXP: 0,
            f.DYNAMIC_FLAGS: 0,
            f.CHANNEL_SPELL: 0,
            f.MOD_CAST_SPEED: 0,
            f.CREATED_BY_SPELL: 0,
            f.NPC_FLAGS: 0,
            f.NPC_EMOTESTATE: 0,
            f.TRAINING_POINTS: 0,
            f.STAT0: 0,
            f.STAT1: 0,
            f.STAT2: 0,
            f.STAT3: 0,
            f.STAT4: 0,
            f.RESISTANCES: 0,
            f.RESISTANCES_01: 0,
            f.RESISTANCES_02: 0,
            f.RESISTANCES_03: 0,
            f.RESISTANCES_04: 0,
            f.RESISTANCES_05: 0,
            f.RESISTANCES_06: 0,
            f.BASE_MANA: 0,
            f.BASE_HEALTH: 0,
            f.BYTES_2: 0,
            f.ATTACK_POWER: 0,
            f.ATTACK_POWER_MODS: 0,
            f.ATTACK_POWER_MULTIPLIER: 0,
            f.RANGED_ATTACK_POWER: 0,
            f.RANGED_ATTACK_POWER_MODS: 0,
            f.RANGED_ATTACK_POWER_MULTIPLIER: 0,
            f.MINRANGEDDAMAGE: 0,
            f.MAXRANGEDDAMAGE: 0,
            f.POWER_COST_MODIFIER: 0,
            f.POWER_COST_MODIFIER_01: 0,
            f.POWER_COST_MODIFIER_02: 0,
            f.POWER_COST_MODIFIER_03: 0,
            f.POWER_COST_MODIFIER_04: 0,
            f.POWER_COST_MODIFIER_05: 0,
            f.POWER_COST_MODIFIER_06: 0,
            f.POWER_COST_MULTIPLIER: 0,
            f.POWER_COST_MULTIPLIER_01: 0,
            f.POWER_COST_MULTIPLIER_02: 0,
            f.POWER_COST_MULTIPLIER_03: 0,
            f.POWER_COST_MULTIPLIER_04: 0,
            f.POWER_COST_MULTIPLIER_05: 0,
            f.POWER_COST_MULTIPLIER_06: 0,
            f.PADDING: 0,
        }

        return {**super(Unit, self).update_fields(), **fields}
