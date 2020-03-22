from typing import Tuple

from pony import orm

from database import constants
from database.db import db


class ItemTemplate(db.Entity):
    """ItemTemplate represents in-game items (including containers).

    Each ItemTemplate corresponds to one item.
    """
    entry = orm.PrimaryKey(int)

    # Reverse attribute: all instances of this template.
    item_backlink = orm.Set('Item')
    npc_main_hands_backlink = orm.Set('Unit', reverse='npc_main_hand')
    npc_off_hands_backlink = orm.Set('Unit', reverse='npc_off_hand')
    npc_rangeds_backlink = orm.Set('Unit', reverse='npc_ranged')

    # TODO: sort these fields, copied from item_template.sql
    class_ = orm.Optional(int)
    subclass = orm.Optional(int)
    name = orm.Optional(str)
    displayid = orm.Optional(int)
    Quality = orm.Optional(int)
    Flags = orm.Optional(int)
    BuyCount = orm.Optional(int)
    BuyPrice = orm.Optional(int)
    SellPrice = orm.Optional(int)
    InventoryType = orm.Optional(int)
    AllowableClass = orm.Optional(int)
    AllowableRace = orm.Optional(int)
    ItemLevel = orm.Optional(int)
    RequiredLevel = orm.Optional(int)
    RequiredSkill = orm.Optional(int)
    RequiredSkillRank = orm.Optional(int)
    requiredspell = orm.Optional(int)
    requiredhonorrank = orm.Optional(int)
    RequiredCityRank = orm.Optional(int)
    RequiredReputationFaction = orm.Optional(int)
    RequiredReputationRank = orm.Optional(int)
    maxcount = orm.Optional(int)
    stackable = orm.Optional(int)
    ContainerSlots = orm.Optional(int)
    stat_type1 = orm.Optional(int)
    stat_value1 = orm.Optional(int)
    stat_type2 = orm.Optional(int)
    stat_value2 = orm.Optional(int)
    stat_type3 = orm.Optional(int)
    stat_value3 = orm.Optional(int)
    stat_type4 = orm.Optional(int)
    stat_value4 = orm.Optional(int)
    stat_type5 = orm.Optional(int)
    stat_value5 = orm.Optional(int)
    stat_type6 = orm.Optional(int)
    stat_value6 = orm.Optional(int)
    stat_type7 = orm.Optional(int)
    stat_value7 = orm.Optional(int)
    stat_type8 = orm.Optional(int)
    stat_value8 = orm.Optional(int)
    stat_type9 = orm.Optional(int)
    stat_value9 = orm.Optional(int)
    stat_type10 = orm.Optional(int)
    stat_value10 = orm.Optional(int)
    dmg_min1 = orm.Optional(float)
    dmg_max1 = orm.Optional(float)
    dmg_type1 = orm.Optional(int)
    dmg_min2 = orm.Optional(float)
    dmg_max2 = orm.Optional(float)
    dmg_type2 = orm.Optional(int)
    dmg_min3 = orm.Optional(float)
    dmg_max3 = orm.Optional(float)
    dmg_type3 = orm.Optional(int)
    dmg_min4 = orm.Optional(float)
    dmg_max4 = orm.Optional(float)
    dmg_type4 = orm.Optional(int)
    dmg_min5 = orm.Optional(float)
    dmg_max5 = orm.Optional(float)
    dmg_type5 = orm.Optional(int)

    def dmg(self, dmg_type: int) -> Tuple[float, float]:
        for i in range(1, 5 + 1):
            if getattr(self, f'dmg_type{i}') == dmg_type:
                return (getattr(self, f'dmg_min{i}'), getattr(self, f'dmg_max{i}'))
        return (0.0, 0.0)

    armor = orm.Optional(int)
    holy_res = orm.Optional(int)
    fire_res = orm.Optional(int)
    nature_res = orm.Optional(int)
    frost_res = orm.Optional(int)
    shadow_res = orm.Optional(int)
    arcane_res = orm.Optional(int)
    delay = orm.Optional(int)
    ammo_type = orm.Optional(int)
    RangedModRange = orm.Optional(int)
    spellid_1 = orm.Optional(int)
    spelltrigger_1 = orm.Optional(int)
    spellcharges_1 = orm.Optional(int)
    spellppmRate_1 = orm.Optional(float)
    spellcooldown_1 = orm.Optional(int)
    spellcategory_1 = orm.Optional(int)
    spellcategorycooldown_1 = orm.Optional(int)
    spellid_2 = orm.Optional(int)
    spelltrigger_2 = orm.Optional(int)
    spellcharges_2 = orm.Optional(int)
    spellppmRate_2 = orm.Optional(float)
    spellcooldown_2 = orm.Optional(int)
    spellcategory_2 = orm.Optional(int)
    spellcategorycooldown_2 = orm.Optional(int)
    spellid_3 = orm.Optional(int)
    spelltrigger_3 = orm.Optional(int)
    spellcharges_3 = orm.Optional(int)
    spellppmRate_3 = orm.Optional(float)
    spellcooldown_3 = orm.Optional(int)
    spellcategory_3 = orm.Optional(int)
    spellcategorycooldown_3 = orm.Optional(int)
    spellid_4 = orm.Optional(int)
    spelltrigger_4 = orm.Optional(int)
    spellcharges_4 = orm.Optional(int)
    spellppmRate_4 = orm.Optional(float)
    spellcooldown_4 = orm.Optional(int)
    spellcategory_4 = orm.Optional(int)
    spellcategorycooldown_4 = orm.Optional(int)
    spellid_5 = orm.Optional(int)
    spelltrigger_5 = orm.Optional(int)
    spellcharges_5 = orm.Optional(int)
    spellppmRate_5 = orm.Optional(float)
    spellcooldown_5 = orm.Optional(int)
    spellcategory_5 = orm.Optional(int)
    spellcategorycooldown_5 = orm.Optional(int)
    bonding = orm.Optional(int)
    description = orm.Optional(str)
    PageText = orm.Optional(int)
    LanguageID = orm.Optional(int)
    PageMaterial = orm.Optional(int)
    startquest = orm.Optional(int)
    lockid = orm.Optional(int)
    Material = orm.Optional(int)
    sheath = orm.Optional(int)
    RandomProperty = orm.Optional(int)
    block = orm.Optional(int)
    itemset = orm.Optional(int)
    MaxDurability = orm.Optional(int)
    area = orm.Optional(int)
    Map = orm.Optional(int)
    BagFamily = orm.Optional(int)
    DisenchantID = orm.Optional(int)
    FoodType = orm.Optional(int)
    minMoneyLoot = orm.Optional(int)
    maxMoneyLoot = orm.Optional(int)
    Duration = orm.Optional(int)
    ExtraFlags = orm.Optional(int)
