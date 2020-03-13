from pony import orm

from database.db import db


class UnitTemplate(db.Entity):
    """UnitTemplate represents in-game units.

    Each UnitTemplate corresponds to one unit. Units include all NPCs (monsters, vendors, ...).
    """
    entry = orm.PrimaryKey(int)

    # Reverse attribute: all instances of this template.
    unit_backlink = orm.Set('Unit')

    # TODO: sort these fields, copied from item_template.sql
    Name = orm.Optional(str)
    SubName = orm.Optional(str)
    MinLevel = orm.Optional(int)
    MaxLevel = orm.Optional(int)
    ModelId1 = orm.Optional('UnitModelInfo', reverse='unit_1_backlink')
    ModelId2 = orm.Optional('UnitModelInfo', reverse='unit_2_backlink')
    ModelId3 = orm.Optional('UnitModelInfo', reverse='unit_3_backlink')
    ModelId4 = orm.Optional('UnitModelInfo', reverse='unit_4_backlink')
    FactionAlliance = orm.Optional(int)
    FactionHorde = orm.Optional(int)
    Scale = orm.Optional(float)
    Family = orm.Optional(int)
    CreatureType = orm.Optional(int)
    InhabitType = orm.Optional(int)
    RegenerateStats = orm.Optional(int)
    RacialLeader = orm.Optional(int)
    NpcFlags = orm.Optional(int)
    UnitFlags = orm.Optional(int)
    DynamicFlags = orm.Optional(int)
    ExtraFlags = orm.Optional(int)
    CreatureTypeFlags = orm.Optional(int)
    SpeedWalk = orm.Optional(float)
    SpeedRun = orm.Optional(float)
    UnitClass = orm.Optional(int)
    Rank = orm.Optional(int)
    HealthMultiplier = orm.Optional(float)
    PowerMultiplier = orm.Optional(float)
    DamageMultiplier = orm.Optional(float)
    DamageVariance = orm.Optional(int)
    ArmorMultiplier = orm.Optional(float)
    ExperienceMultiplier = orm.Optional(float)
    MinLevelHealth = orm.Optional(int)
    MaxLevelHealth = orm.Optional(int)
    MinLevelMana = orm.Optional(int)
    MaxLevelMana = orm.Optional(int)
    MinMeleeDmg = orm.Optional(float)
    MaxMeleeDmg = orm.Optional(float)
    MinRangedDmg = orm.Optional(float)
    MaxRangedDmg = orm.Optional(float)
    Armor = orm.Optional(int)
    MeleeAttackPower = orm.Optional(int)
    RangedAttackPower = orm.Optional(int)
    MeleeBaseAttackTime = orm.Optional(int)
    RangedBaseAttackTime = orm.Optional(int)
    DamageSchool = orm.Optional(int)
    MinLootGold = orm.Optional(int)
    MaxLootGold = orm.Optional(int)
    LootId = orm.Optional(int)
    PickpocketLootId = orm.Optional(int)
    SkinningLootId = orm.Optional(int)
    KillCredit1 = orm.Optional(int)
    KillCredit2 = orm.Optional(int)
    MechanicImmuneMask = orm.Optional(int)
    SchoolImmuneMask = orm.Optional(int)
    ResistanceHoly = orm.Optional(int)
    ResistanceFire = orm.Optional(int)
    ResistanceNature = orm.Optional(int)
    ResistanceFrost = orm.Optional(int)
    ResistanceShadow = orm.Optional(int)
    ResistanceArcane = orm.Optional(int)
    PetSpellDataId = orm.Optional(int)
    MovementType = orm.Optional(int)
    TrainerType = orm.Optional(int)
    TrainerSpell = orm.Optional(int)
    TrainerClass = orm.Optional(int)
    TrainerRace = orm.Optional(int)
    TrainerTemplateId = orm.Optional(int)
    VendorTemplateId = orm.Optional(int)
    GossipMenuId = orm.Optional(int)
    EquipmentTemplateId = orm.Optional(int)
    Civilian = orm.Optional(int)
    AIName = orm.Optional(str)