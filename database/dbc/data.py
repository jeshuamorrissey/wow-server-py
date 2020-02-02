import gzip
import json
import logging

from pony import orm

from database.dbc import constants as c
from database.dbc.char_start_outfit import CharStartOutfit
from database.dbc.chr_start_locations import ChrStartLocation
from database.dbc.item_template import ItemTemplate
from database.dbc.unit_template import UnitTemplate


@orm.db_session
def LoadDBC():
    # yapf: disable
    logging.info('Loading ChrStartLocation...')
    ChrStartLocation(race=c.Race.HUMAN, map=0, zone=12, x=-8949.95, y=-132.493, z=83.5312, o=0.0)
    ChrStartLocation(race=c.Race.ORC, map=1, zone=14, x=-618.518, y=-4251.67, z=38.718, o=0.0)
    ChrStartLocation(race=c.Race.DWARF, map=0, zone=1, x=-6240.32, y=331.033, z=382.758, o=6.17716)
    ChrStartLocation(race=c.Race.NIGHTELF, map=1, zone=141, x=10311.3, y=832.463, z=1326.41, o=5.69632)
    ChrStartLocation(race=c.Race.UNDEAD, map=0, zone=85, x=1676.71, y=1678.31, z=121.67, o=2.70526)
    ChrStartLocation(race=c.Race.TAUREN, map=1, zone=215, x=-2917.58, y=-257.98, z=52.9968, o=0.0)
    ChrStartLocation(race=c.Race.GNOME, map=0, zone=1, x=-6240.32, y=331.033, z=382.758, o=0.0)
    ChrStartLocation(race=c.Race.TROLL, map=1, zone=14, x=-618.518, y=-4251.67, z=38.718, o=0.0)

    logging.info('Loading CharStartOutfit...')
    CharStartOutfit(race=c.Race.HUMAN, class_=c.Class.WARRIOR, gender=c.Gender.MALE, equipment=[{'entry': 38, 'equipment_slot': 'BODY'}, {'entry': 39, 'equipment_slot': 'LEGS'}, {'entry': 40, 'equipment_slot': 'FEET'}, {'entry': 25, 'equipment_slot': 'MAIN_HAND'}, {'entry': 2362, 'equipment_slot': 'OFF_HAND'}], items=[117, 6948])
    CharStartOutfit(race=c.Race.HUMAN, class_=c.Class.WARRIOR, gender=c.Gender.FEMALE, equipment=[{'entry': 38, 'equipment_slot': 'BODY'}, {'entry': 39, 'equipment_slot': 'LEGS'}, {'entry': 40, 'equipment_slot': 'FEET'}, {'entry': 25, 'equipment_slot': 'MAIN_HAND'}, {'entry': 2362, 'equipment_slot': 'OFF_HAND'}], items=[117, 6948])
    CharStartOutfit(race=c.Race.HUMAN, class_=c.Class.PALADIN, gender=c.Gender.MALE, equipment=[{'entry': 45, 'equipment_slot': 'BODY'}, {'entry': 43, 'equipment_slot': 'FEET'}, {'entry': 44, 'equipment_slot': 'LEGS'}, {'entry': 2361, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 159, 2070])
    CharStartOutfit(race=c.Race.HUMAN, class_=c.Class.PALADIN, gender=c.Gender.FEMALE, equipment=[{'entry': 45, 'equipment_slot': 'BODY'}, {'entry': 43, 'equipment_slot': 'FEET'}, {'entry': 44, 'equipment_slot': 'LEGS'}, {'entry': 2361, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 159, 2070])
    CharStartOutfit(race=c.Race.HUMAN, class_=c.Class.ROGUE, gender=c.Gender.MALE, equipment=[{'entry': 49, 'equipment_slot': 'BODY'}, {'entry': 47, 'equipment_slot': 'FEET'}, {'entry': 48, 'equipment_slot': 'LEGS'}, {'entry': 2947, 'equipment_slot': 'RANGED'}, {'entry': 2092, 'equipment_slot': 'MAIN_HAND'}], items=[2070, 6948])
    CharStartOutfit(race=c.Race.HUMAN, class_=c.Class.ROGUE, gender=c.Gender.FEMALE, equipment=[{'entry': 49, 'equipment_slot': 'BODY'}, {'entry': 47, 'equipment_slot': 'FEET'}, {'entry': 48, 'equipment_slot': 'LEGS'}, {'entry': 2947, 'equipment_slot': 'RANGED'}, {'entry': 2092, 'equipment_slot': 'MAIN_HAND'}], items=[2070, 6948])
    CharStartOutfit(race=c.Race.HUMAN, class_=c.Class.PRIEST, gender=c.Gender.MALE, equipment=[{'entry': 6098, 'equipment_slot': 'CHEST'}, {'entry': 52, 'equipment_slot': 'LEGS'}, {'entry': 53, 'equipment_slot': 'BODY'}, {'entry': 51, 'equipment_slot': 'FEET'}, {'entry': 36, 'equipment_slot': 'MAIN_HAND'}], items=[159, 2070, 6948])
    CharStartOutfit(race=c.Race.HUMAN, class_=c.Class.PRIEST, gender=c.Gender.FEMALE, equipment=[{'entry': 6098, 'equipment_slot': 'CHEST'}, {'entry': 52, 'equipment_slot': 'LEGS'}, {'entry': 53, 'equipment_slot': 'BODY'}, {'entry': 51, 'equipment_slot': 'FEET'}, {'entry': 36, 'equipment_slot': 'MAIN_HAND'}], items=[159, 2070, 6948])
    CharStartOutfit(race=c.Race.HUMAN, class_=c.Class.MAGE, gender=c.Gender.MALE, equipment=[{'entry': 56, 'equipment_slot': 'CHEST'}, {'entry': 1395, 'equipment_slot': 'LEGS'}, {'entry': 55, 'equipment_slot': 'FEET'}, {'entry': 35, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6096, 'equipment_slot': 'BODY'}], items=[2070, 159, 6948])
    CharStartOutfit(race=c.Race.HUMAN, class_=c.Class.MAGE, gender=c.Gender.FEMALE, equipment=[{'entry': 56, 'equipment_slot': 'CHEST'}, {'entry': 1395, 'equipment_slot': 'LEGS'}, {'entry': 55, 'equipment_slot': 'FEET'}, {'entry': 35, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6096, 'equipment_slot': 'BODY'}], items=[2070, 159, 6948])
    CharStartOutfit(race=c.Race.HUMAN, class_=c.Class.WARLOCK, gender=c.Gender.MALE, equipment=[{'entry': 57, 'equipment_slot': 'CHEST'}, {'entry': 6097, 'equipment_slot': 'BODY'}, {'entry': 1396, 'equipment_slot': 'LEGS'}, {'entry': 2092, 'equipment_slot': 'MAIN_HAND'}, {'entry': 59, 'equipment_slot': 'FEET'}], items=[4604, 159, 6948])
    CharStartOutfit(race=c.Race.HUMAN, class_=c.Class.WARLOCK, gender=c.Gender.FEMALE, equipment=[{'entry': 57, 'equipment_slot': 'CHEST'}, {'entry': 6097, 'equipment_slot': 'BODY'}, {'entry': 1396, 'equipment_slot': 'LEGS'}, {'entry': 2092, 'equipment_slot': 'MAIN_HAND'}, {'entry': 59, 'equipment_slot': 'FEET'}], items=[4604, 159, 6948])
    CharStartOutfit(race=c.Race.ORC, class_=c.Class.WARRIOR, gender=c.Gender.MALE, equipment=[{'entry': 6125, 'equipment_slot': 'BODY'}, {'entry': 139, 'equipment_slot': 'LEGS'}, {'entry': 140, 'equipment_slot': 'FEET'}, {'entry': 12282, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 117])
    CharStartOutfit(race=c.Race.ORC, class_=c.Class.WARRIOR, gender=c.Gender.FEMALE, equipment=[{'entry': 6125, 'equipment_slot': 'BODY'}, {'entry': 139, 'equipment_slot': 'LEGS'}, {'entry': 140, 'equipment_slot': 'FEET'}, {'entry': 12282, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 117])
    CharStartOutfit(race=c.Race.ORC, class_=c.Class.HUNTER, gender=c.Gender.MALE, equipment=[{'entry': 127, 'equipment_slot': 'BODY'}, {'entry': 6126, 'equipment_slot': 'LEGS'}, {'entry': 6127, 'equipment_slot': 'FEET'}, {'entry': 37, 'equipment_slot': 'MAIN_HAND'}, {'entry': 2504, 'equipment_slot': 'RANGED'}], items=[159, 6948, 2101, 117, 2512])
    CharStartOutfit(race=c.Race.ORC, class_=c.Class.HUNTER, gender=c.Gender.FEMALE, equipment=[{'entry': 127, 'equipment_slot': 'BODY'}, {'entry': 6126, 'equipment_slot': 'LEGS'}, {'entry': 6127, 'equipment_slot': 'FEET'}, {'entry': 37, 'equipment_slot': 'MAIN_HAND'}, {'entry': 2504, 'equipment_slot': 'RANGED'}], items=[159, 6948, 2101, 117, 2512])
    CharStartOutfit(race=c.Race.ORC, class_=c.Class.ROGUE, gender=c.Gender.MALE, equipment=[{'entry': 2105, 'equipment_slot': 'BODY'}, {'entry': 120, 'equipment_slot': 'LEGS'}, {'entry': 121, 'equipment_slot': 'FEET'}, {'entry': 3111, 'equipment_slot': 'RANGED'}, {'entry': 2092, 'equipment_slot': 'MAIN_HAND'}], items=[117, 6948])
    CharStartOutfit(race=c.Race.ORC, class_=c.Class.ROGUE, gender=c.Gender.FEMALE, equipment=[{'entry': 2105, 'equipment_slot': 'BODY'}, {'entry': 120, 'equipment_slot': 'LEGS'}, {'entry': 121, 'equipment_slot': 'FEET'}, {'entry': 3111, 'equipment_slot': 'RANGED'}, {'entry': 2092, 'equipment_slot': 'MAIN_HAND'}], items=[117, 6948])
    CharStartOutfit(race=c.Race.ORC, class_=c.Class.SHAMAN, gender=c.Gender.MALE, equipment=[{'entry': 154, 'equipment_slot': 'BODY'}, {'entry': 153, 'equipment_slot': 'LEGS'}, {'entry': 36, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 117, 159])
    CharStartOutfit(race=c.Race.ORC, class_=c.Class.SHAMAN, gender=c.Gender.FEMALE, equipment=[{'entry': 154, 'equipment_slot': 'BODY'}, {'entry': 153, 'equipment_slot': 'LEGS'}, {'entry': 36, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 117, 159])
    CharStartOutfit(race=c.Race.ORC, class_=c.Class.WARLOCK, gender=c.Gender.MALE, equipment=[{'entry': 6129, 'equipment_slot': 'CHEST'}, {'entry': 1396, 'equipment_slot': 'LEGS'}, {'entry': 59, 'equipment_slot': 'FEET'}, {'entry': 2092, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 117, 159])
    CharStartOutfit(race=c.Race.ORC, class_=c.Class.WARLOCK, gender=c.Gender.FEMALE, equipment=[{'entry': 6129, 'equipment_slot': 'CHEST'}, {'entry': 1396, 'equipment_slot': 'LEGS'}, {'entry': 59, 'equipment_slot': 'FEET'}, {'entry': 2092, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 117, 159])
    CharStartOutfit(race=c.Race.DWARF, class_=c.Class.WARRIOR, gender=c.Gender.MALE, equipment=[{'entry': 38, 'equipment_slot': 'BODY'}, {'entry': 39, 'equipment_slot': 'LEGS'}, {'entry': 40, 'equipment_slot': 'FEET'}, {'entry': 12282, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 117])
    CharStartOutfit(race=c.Race.DWARF, class_=c.Class.WARRIOR, gender=c.Gender.FEMALE, equipment=[{'entry': 38, 'equipment_slot': 'BODY'}, {'entry': 39, 'equipment_slot': 'LEGS'}, {'entry': 40, 'equipment_slot': 'FEET'}, {'entry': 12282, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 117])
    CharStartOutfit(race=c.Race.DWARF, class_=c.Class.PALADIN, gender=c.Gender.MALE, equipment=[{'entry': 6117, 'equipment_slot': 'BODY'}, {'entry': 6118, 'equipment_slot': 'LEGS'}, {'entry': 43, 'equipment_slot': 'FEET'}, {'entry': 2361, 'equipment_slot': 'MAIN_HAND'}], items=[4540, 159, 6948])
    CharStartOutfit(race=c.Race.DWARF, class_=c.Class.PALADIN, gender=c.Gender.FEMALE, equipment=[{'entry': 6117, 'equipment_slot': 'BODY'}, {'entry': 6118, 'equipment_slot': 'LEGS'}, {'entry': 43, 'equipment_slot': 'FEET'}, {'entry': 2361, 'equipment_slot': 'MAIN_HAND'}], items=[4540, 159, 6948])
    CharStartOutfit(race=c.Race.DWARF, class_=c.Class.HUNTER, gender=c.Gender.MALE, equipment=[{'entry': 148, 'equipment_slot': 'BODY'}, {'entry': 147, 'equipment_slot': 'LEGS'}, {'entry': 129, 'equipment_slot': 'FEET'}, {'entry': 37, 'equipment_slot': 'MAIN_HAND'}], items=[159, 2102, 2508, 2516, 117, 6948])
    CharStartOutfit(race=c.Race.DWARF, class_=c.Class.HUNTER, gender=c.Gender.FEMALE, equipment=[{'entry': 148, 'equipment_slot': 'BODY'}, {'entry': 147, 'equipment_slot': 'LEGS'}, {'entry': 129, 'equipment_slot': 'FEET'}, {'entry': 37, 'equipment_slot': 'MAIN_HAND'}], items=[159, 2102, 2508, 2516, 117, 6948])
    CharStartOutfit(race=c.Race.DWARF, class_=c.Class.ROGUE, gender=c.Gender.MALE, equipment=[{'entry': 2092, 'equipment_slot': 'MAIN_HAND'}, {'entry': 49, 'equipment_slot': 'BODY'}, {'entry': 48, 'equipment_slot': 'LEGS'}, {'entry': 47, 'equipment_slot': 'FEET'}, {'entry': 3111, 'equipment_slot': 'RANGED'}], items=[4540, 6948])
    CharStartOutfit(race=c.Race.DWARF, class_=c.Class.ROGUE, gender=c.Gender.FEMALE, equipment=[{'entry': 2092, 'equipment_slot': 'MAIN_HAND'}, {'entry': 49, 'equipment_slot': 'BODY'}, {'entry': 48, 'equipment_slot': 'LEGS'}, {'entry': 47, 'equipment_slot': 'FEET'}, {'entry': 3111, 'equipment_slot': 'RANGED'}], items=[4540, 6948])
    CharStartOutfit(race=c.Race.DWARF, class_=c.Class.PRIEST, gender=c.Gender.MALE, equipment=[{'entry': 6098, 'equipment_slot': 'CHEST'}, {'entry': 53, 'equipment_slot': 'BODY'}, {'entry': 52, 'equipment_slot': 'LEGS'}, {'entry': 51, 'equipment_slot': 'FEET'}, {'entry': 36, 'equipment_slot': 'MAIN_HAND'}], items=[159, 4540, 6948])
    CharStartOutfit(race=c.Race.DWARF, class_=c.Class.PRIEST, gender=c.Gender.FEMALE, equipment=[{'entry': 6098, 'equipment_slot': 'CHEST'}, {'entry': 53, 'equipment_slot': 'BODY'}, {'entry': 52, 'equipment_slot': 'LEGS'}, {'entry': 51, 'equipment_slot': 'FEET'}, {'entry': 36, 'equipment_slot': 'MAIN_HAND'}], items=[159, 4540, 6948])
    CharStartOutfit(race=c.Race.DWARF, class_=c.Class.MAGE, gender=c.Gender.MALE, equipment=[{'entry': 6116, 'equipment_slot': 'CHEST'}, {'entry': 1395, 'equipment_slot': 'LEGS'}, {'entry': 6096, 'equipment_slot': 'BODY'}, {'entry': 35, 'equipment_slot': 'MAIN_HAND'}, {'entry': 55, 'equipment_slot': 'FEET'}], items=[159, 4540, 6948])
    CharStartOutfit(race=c.Race.DWARF, class_=c.Class.MAGE, gender=c.Gender.FEMALE, equipment=[{'entry': 6116, 'equipment_slot': 'CHEST'}, {'entry': 1395, 'equipment_slot': 'LEGS'}, {'entry': 6096, 'equipment_slot': 'BODY'}, {'entry': 35, 'equipment_slot': 'MAIN_HAND'}, {'entry': 55, 'equipment_slot': 'FEET'}], items=[159, 4540, 6948])
    CharStartOutfit(race=c.Race.NIGHTELF, class_=c.Class.WARRIOR, gender=c.Gender.MALE, equipment=[{'entry': 25, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6120, 'equipment_slot': 'BODY'}, {'entry': 6121, 'equipment_slot': 'LEGS'}, {'entry': 6122, 'equipment_slot': 'FEET'}, {'entry': 2362, 'equipment_slot': 'OFF_HAND'}], items=[117, 6948])
    CharStartOutfit(race=c.Race.NIGHTELF, class_=c.Class.WARRIOR, gender=c.Gender.FEMALE, equipment=[{'entry': 25, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6120, 'equipment_slot': 'BODY'}, {'entry': 6121, 'equipment_slot': 'LEGS'}, {'entry': 6122, 'equipment_slot': 'FEET'}, {'entry': 2362, 'equipment_slot': 'OFF_HAND'}], items=[117, 6948])
    CharStartOutfit(race=c.Race.NIGHTELF, class_=c.Class.HUNTER, gender=c.Gender.MALE, equipment=[{'entry': 2092, 'equipment_slot': 'MAIN_HAND'}, {'entry': 148, 'equipment_slot': 'BODY'}, {'entry': 147, 'equipment_slot': 'LEGS'}, {'entry': 129, 'equipment_slot': 'FEET'}, {'entry': 2504, 'equipment_slot': 'RANGED'}], items=[159, 2101, 2512, 117, 6948])
    CharStartOutfit(race=c.Race.NIGHTELF, class_=c.Class.HUNTER, gender=c.Gender.FEMALE, equipment=[{'entry': 2092, 'equipment_slot': 'MAIN_HAND'}, {'entry': 148, 'equipment_slot': 'BODY'}, {'entry': 147, 'equipment_slot': 'LEGS'}, {'entry': 129, 'equipment_slot': 'FEET'}, {'entry': 2504, 'equipment_slot': 'RANGED'}], items=[159, 2101, 2512, 117, 6948])
    CharStartOutfit(race=c.Race.NIGHTELF, class_=c.Class.ROGUE, gender=c.Gender.MALE, equipment=[{'entry': 2092, 'equipment_slot': 'MAIN_HAND'}, {'entry': 49, 'equipment_slot': 'BODY'}, {'entry': 48, 'equipment_slot': 'LEGS'}, {'entry': 47, 'equipment_slot': 'FEET'}, {'entry': 2947, 'equipment_slot': 'RANGED'}], items=[4540, 6948])
    CharStartOutfit(race=c.Race.NIGHTELF, class_=c.Class.ROGUE, gender=c.Gender.FEMALE, equipment=[{'entry': 2092, 'equipment_slot': 'MAIN_HAND'}, {'entry': 49, 'equipment_slot': 'BODY'}, {'entry': 48, 'equipment_slot': 'LEGS'}, {'entry': 47, 'equipment_slot': 'FEET'}, {'entry': 2947, 'equipment_slot': 'RANGED'}], items=[4540, 6948])
    CharStartOutfit(race=c.Race.NIGHTELF, class_=c.Class.PRIEST, gender=c.Gender.MALE, equipment=[{'entry': 36, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6119, 'equipment_slot': 'CHEST'}, {'entry': 52, 'equipment_slot': 'LEGS'}, {'entry': 51, 'equipment_slot': 'FEET'}, {'entry': 53, 'equipment_slot': 'BODY'}], items=[2070, 159, 6948])
    CharStartOutfit(race=c.Race.NIGHTELF, class_=c.Class.PRIEST, gender=c.Gender.FEMALE, equipment=[{'entry': 36, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6119, 'equipment_slot': 'CHEST'}, {'entry': 52, 'equipment_slot': 'LEGS'}, {'entry': 51, 'equipment_slot': 'FEET'}, {'entry': 53, 'equipment_slot': 'BODY'}], items=[2070, 159, 6948])
    CharStartOutfit(race=c.Race.NIGHTELF, class_=c.Class.DRUID, gender=c.Gender.MALE, equipment=[{'entry': 3661, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6123, 'equipment_slot': 'CHEST'}, {'entry': 6124, 'equipment_slot': 'LEGS'}], items=[159, 4536, 6948])
    CharStartOutfit(race=c.Race.NIGHTELF, class_=c.Class.DRUID, gender=c.Gender.FEMALE, equipment=[{'entry': 3661, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6123, 'equipment_slot': 'CHEST'}, {'entry': 6124, 'equipment_slot': 'LEGS'}], items=[159, 4536, 6948])
    CharStartOutfit(race=c.Race.UNDEAD, class_=c.Class.WARRIOR, gender=c.Gender.MALE, equipment=[{'entry': 6125, 'equipment_slot': 'BODY'}, {'entry': 139, 'equipment_slot': 'LEGS'}, {'entry': 140, 'equipment_slot': 'FEET'}, {'entry': 25, 'equipment_slot': 'MAIN_HAND'}, {'entry': 2362, 'equipment_slot': 'OFF_HAND'}], items=[4604, 6948])
    CharStartOutfit(race=c.Race.UNDEAD, class_=c.Class.WARRIOR, gender=c.Gender.FEMALE, equipment=[{'entry': 6125, 'equipment_slot': 'BODY'}, {'entry': 139, 'equipment_slot': 'LEGS'}, {'entry': 140, 'equipment_slot': 'FEET'}, {'entry': 25, 'equipment_slot': 'MAIN_HAND'}, {'entry': 2362, 'equipment_slot': 'OFF_HAND'}], items=[4604, 6948])
    CharStartOutfit(race=c.Race.UNDEAD, class_=c.Class.ROGUE, gender=c.Gender.MALE, equipment=[{'entry': 2092, 'equipment_slot': 'MAIN_HAND'}, {'entry': 2105, 'equipment_slot': 'BODY'}, {'entry': 120, 'equipment_slot': 'LEGS'}, {'entry': 121, 'equipment_slot': 'FEET'}, {'entry': 2947, 'equipment_slot': 'RANGED'}], items=[4604, 6948])
    CharStartOutfit(race=c.Race.UNDEAD, class_=c.Class.ROGUE, gender=c.Gender.FEMALE, equipment=[{'entry': 2092, 'equipment_slot': 'MAIN_HAND'}, {'entry': 2105, 'equipment_slot': 'BODY'}, {'entry': 120, 'equipment_slot': 'LEGS'}, {'entry': 121, 'equipment_slot': 'FEET'}, {'entry': 2947, 'equipment_slot': 'RANGED'}], items=[4604, 6948])
    CharStartOutfit(race=c.Race.UNDEAD, class_=c.Class.PRIEST, gender=c.Gender.MALE, equipment=[{'entry': 6144, 'equipment_slot': 'CHEST'}, {'entry': 53, 'equipment_slot': 'BODY'}, {'entry': 52, 'equipment_slot': 'LEGS'}, {'entry': 36, 'equipment_slot': 'MAIN_HAND'}, {'entry': 51, 'equipment_slot': 'FEET'}], items=[4604, 159, 6948])
    CharStartOutfit(race=c.Race.UNDEAD, class_=c.Class.PRIEST, gender=c.Gender.FEMALE, equipment=[{'entry': 6144, 'equipment_slot': 'CHEST'}, {'entry': 53, 'equipment_slot': 'BODY'}, {'entry': 52, 'equipment_slot': 'LEGS'}, {'entry': 36, 'equipment_slot': 'MAIN_HAND'}, {'entry': 51, 'equipment_slot': 'FEET'}], items=[4604, 159, 6948])
    CharStartOutfit(race=c.Race.UNDEAD, class_=c.Class.MAGE, gender=c.Gender.MALE, equipment=[{'entry': 6140, 'equipment_slot': 'CHEST'}, {'entry': 1395, 'equipment_slot': 'LEGS'}, {'entry': 6096, 'equipment_slot': 'BODY'}, {'entry': 35, 'equipment_slot': 'MAIN_HAND'}, {'entry': 55, 'equipment_slot': 'FEET'}], items=[4604, 159, 6948])
    CharStartOutfit(race=c.Race.UNDEAD, class_=c.Class.MAGE, gender=c.Gender.FEMALE, equipment=[{'entry': 6140, 'equipment_slot': 'CHEST'}, {'entry': 1395, 'equipment_slot': 'LEGS'}, {'entry': 6096, 'equipment_slot': 'BODY'}, {'entry': 35, 'equipment_slot': 'MAIN_HAND'}, {'entry': 55, 'equipment_slot': 'FEET'}], items=[4604, 159, 6948])
    CharStartOutfit(race=c.Race.UNDEAD, class_=c.Class.WARLOCK, gender=c.Gender.MALE, equipment=[{'entry': 6129, 'equipment_slot': 'CHEST'}, {'entry': 1396, 'equipment_slot': 'LEGS'}, {'entry': 59, 'equipment_slot': 'FEET'}, {'entry': 2092, 'equipment_slot': 'MAIN_HAND'}], items=[4604, 159, 6948])
    CharStartOutfit(race=c.Race.UNDEAD, class_=c.Class.WARLOCK, gender=c.Gender.FEMALE, equipment=[{'entry': 6129, 'equipment_slot': 'CHEST'}, {'entry': 1396, 'equipment_slot': 'LEGS'}, {'entry': 59, 'equipment_slot': 'FEET'}, {'entry': 2092, 'equipment_slot': 'MAIN_HAND'}], items=[4604, 159, 6948])
    CharStartOutfit(race=c.Race.TAUREN, class_=c.Class.WARRIOR, gender=c.Gender.MALE, equipment=[{'entry': 6125, 'equipment_slot': 'BODY'}, {'entry': 139, 'equipment_slot': 'LEGS'}, {'entry': 2361, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 4540])
    CharStartOutfit(race=c.Race.TAUREN, class_=c.Class.WARRIOR, gender=c.Gender.FEMALE, equipment=[{'entry': 6125, 'equipment_slot': 'BODY'}, {'entry': 139, 'equipment_slot': 'LEGS'}, {'entry': 2361, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 4540])
    CharStartOutfit(race=c.Race.TAUREN, class_=c.Class.HUNTER, gender=c.Gender.MALE, equipment=[{'entry': 127, 'equipment_slot': 'BODY'}, {'entry': 6126, 'equipment_slot': 'LEGS'}, {'entry': 37, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 159, 2508, 2102, 2516, 117])
    CharStartOutfit(race=c.Race.TAUREN, class_=c.Class.HUNTER, gender=c.Gender.FEMALE, equipment=[{'entry': 127, 'equipment_slot': 'BODY'}, {'entry': 6126, 'equipment_slot': 'LEGS'}, {'entry': 37, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 159, 2508, 2102, 2516, 117])
    CharStartOutfit(race=c.Race.TAUREN, class_=c.Class.SHAMAN, gender=c.Gender.MALE, equipment=[{'entry': 154, 'equipment_slot': 'BODY'}, {'entry': 153, 'equipment_slot': 'LEGS'}, {'entry': 36, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 4604, 159])
    CharStartOutfit(race=c.Race.TAUREN, class_=c.Class.SHAMAN, gender=c.Gender.FEMALE, equipment=[{'entry': 154, 'equipment_slot': 'BODY'}, {'entry': 153, 'equipment_slot': 'LEGS'}, {'entry': 36, 'equipment_slot': 'MAIN_HAND'}], items=[6948, 4604, 159])
    CharStartOutfit(race=c.Race.TAUREN, class_=c.Class.DRUID, gender=c.Gender.MALE, equipment=[{'entry': 35, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6139, 'equipment_slot': 'CHEST'}, {'entry': 6124, 'equipment_slot': 'LEGS'}], items=[159, 4536, 6948])
    CharStartOutfit(race=c.Race.TAUREN, class_=c.Class.DRUID, gender=c.Gender.FEMALE, equipment=[{'entry': 35, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6139, 'equipment_slot': 'CHEST'}, {'entry': 6124, 'equipment_slot': 'LEGS'}], items=[159, 4536, 6948])
    CharStartOutfit(race=c.Race.GNOME, class_=c.Class.WARRIOR, gender=c.Gender.MALE, equipment=[{'entry': 38, 'equipment_slot': 'BODY'}, {'entry': 39, 'equipment_slot': 'LEGS'}, {'entry': 40, 'equipment_slot': 'FEET'}, {'entry': 25, 'equipment_slot': 'MAIN_HAND'}, {'entry': 2362, 'equipment_slot': 'OFF_HAND'}], items=[117, 6948])
    CharStartOutfit(race=c.Race.GNOME, class_=c.Class.WARRIOR, gender=c.Gender.FEMALE, equipment=[{'entry': 38, 'equipment_slot': 'BODY'}, {'entry': 39, 'equipment_slot': 'LEGS'}, {'entry': 40, 'equipment_slot': 'FEET'}, {'entry': 25, 'equipment_slot': 'MAIN_HAND'}, {'entry': 2362, 'equipment_slot': 'OFF_HAND'}], items=[117, 6948])
    CharStartOutfit(race=c.Race.GNOME, class_=c.Class.ROGUE, gender=c.Gender.MALE, equipment=[{'entry': 49, 'equipment_slot': 'BODY'}, {'entry': 48, 'equipment_slot': 'LEGS'}, {'entry': 47, 'equipment_slot': 'FEET'}, {'entry': 2092, 'equipment_slot': 'MAIN_HAND'}, {'entry': 2947, 'equipment_slot': 'RANGED'}], items=[117, 6948])
    CharStartOutfit(race=c.Race.GNOME, class_=c.Class.ROGUE, gender=c.Gender.FEMALE, equipment=[{'entry': 49, 'equipment_slot': 'BODY'}, {'entry': 48, 'equipment_slot': 'LEGS'}, {'entry': 47, 'equipment_slot': 'FEET'}, {'entry': 2092, 'equipment_slot': 'MAIN_HAND'}, {'entry': 2947, 'equipment_slot': 'RANGED'}], items=[117, 6948])
    CharStartOutfit(race=c.Race.GNOME, class_=c.Class.MAGE, gender=c.Gender.MALE, equipment=[{'entry': 56, 'equipment_slot': 'CHEST'}, {'entry': 1395, 'equipment_slot': 'LEGS'}, {'entry': 6096, 'equipment_slot': 'BODY'}, {'entry': 55, 'equipment_slot': 'FEET'}, {'entry': 35, 'equipment_slot': 'MAIN_HAND'}], items=[4536, 159, 6948])
    CharStartOutfit(race=c.Race.GNOME, class_=c.Class.MAGE, gender=c.Gender.FEMALE, equipment=[{'entry': 56, 'equipment_slot': 'CHEST'}, {'entry': 1395, 'equipment_slot': 'LEGS'}, {'entry': 6096, 'equipment_slot': 'BODY'}, {'entry': 55, 'equipment_slot': 'FEET'}, {'entry': 35, 'equipment_slot': 'MAIN_HAND'}], items=[4536, 159, 6948])
    CharStartOutfit(race=c.Race.GNOME, class_=c.Class.WARLOCK, gender=c.Gender.MALE, equipment=[{'entry': 57, 'equipment_slot': 'CHEST'}, {'entry': 6097, 'equipment_slot': 'BODY'}, {'entry': 1396, 'equipment_slot': 'LEGS'}, {'entry': 59, 'equipment_slot': 'FEET'}, {'entry': 2092, 'equipment_slot': 'MAIN_HAND'}], items=[159, 4604, 6948])
    CharStartOutfit(race=c.Race.GNOME, class_=c.Class.WARLOCK, gender=c.Gender.FEMALE, equipment=[{'entry': 57, 'equipment_slot': 'CHEST'}, {'entry': 6097, 'equipment_slot': 'BODY'}, {'entry': 1396, 'equipment_slot': 'LEGS'}, {'entry': 59, 'equipment_slot': 'FEET'}, {'entry': 2092, 'equipment_slot': 'MAIN_HAND'}], items=[159, 4604, 6948])
    CharStartOutfit(race=c.Race.TROLL, class_=c.Class.WARRIOR, gender=c.Gender.MALE, equipment=[{'entry': 37, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6125, 'equipment_slot': 'BODY'}, {'entry': 139, 'equipment_slot': 'LEGS'}, {'entry': 2362, 'equipment_slot': 'OFF_HAND'}, {'entry': 3111, 'equipment_slot': 'RANGED'}], items=[117, 6948])
    CharStartOutfit(race=c.Race.TROLL, class_=c.Class.WARRIOR, gender=c.Gender.FEMALE, equipment=[{'entry': 37, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6125, 'equipment_slot': 'BODY'}, {'entry': 139, 'equipment_slot': 'LEGS'}, {'entry': 2362, 'equipment_slot': 'OFF_HAND'}, {'entry': 3111, 'equipment_slot': 'RANGED'}], items=[117, 6948])
    CharStartOutfit(race=c.Race.TROLL, class_=c.Class.HUNTER, gender=c.Gender.MALE, equipment=[{'entry': 37, 'equipment_slot': 'MAIN_HAND'}, {'entry': 2504, 'equipment_slot': 'RANGED'}, {'entry': 6126, 'equipment_slot': 'LEGS'}, {'entry': 127, 'equipment_slot': 'BODY'}], items=[4604, 2101, 2512, 159, 6948])
    CharStartOutfit(race=c.Race.TROLL, class_=c.Class.HUNTER, gender=c.Gender.FEMALE, equipment=[{'entry': 37, 'equipment_slot': 'MAIN_HAND'}, {'entry': 2504, 'equipment_slot': 'RANGED'}, {'entry': 6126, 'equipment_slot': 'LEGS'}, {'entry': 127, 'equipment_slot': 'BODY'}], items=[4604, 2101, 2512, 159, 6948])
    CharStartOutfit(race=c.Race.TROLL, class_=c.Class.ROGUE, gender=c.Gender.MALE, equipment=[{'entry': 2092, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6136, 'equipment_slot': 'BODY'}, {'entry': 6137, 'equipment_slot': 'LEGS'}, {'entry': 6138, 'equipment_slot': 'FEET'}, {'entry': 3111, 'equipment_slot': 'RANGED'}], items=[117, 6948])
    CharStartOutfit(race=c.Race.TROLL, class_=c.Class.ROGUE, gender=c.Gender.FEMALE, equipment=[{'entry': 2092, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6136, 'equipment_slot': 'BODY'}, {'entry': 6137, 'equipment_slot': 'LEGS'}, {'entry': 6138, 'equipment_slot': 'FEET'}, {'entry': 3111, 'equipment_slot': 'RANGED'}], items=[117, 6948])
    CharStartOutfit(race=c.Race.TROLL, class_=c.Class.PRIEST, gender=c.Gender.MALE, equipment=[{'entry': 36, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6144, 'equipment_slot': 'CHEST'}, {'entry': 53, 'equipment_slot': 'BODY'}, {'entry': 52, 'equipment_slot': 'LEGS'}], items=[4540, 159, 6948])
    CharStartOutfit(race=c.Race.TROLL, class_=c.Class.PRIEST, gender=c.Gender.FEMALE, equipment=[{'entry': 36, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6144, 'equipment_slot': 'CHEST'}, {'entry': 53, 'equipment_slot': 'BODY'}, {'entry': 52, 'equipment_slot': 'LEGS'}], items=[4540, 159, 6948])
    CharStartOutfit(race=c.Race.TROLL, class_=c.Class.SHAMAN, gender=c.Gender.MALE, equipment=[{'entry': 36, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6134, 'equipment_slot': 'BODY'}, {'entry': 6135, 'equipment_slot': 'LEGS'}], items=[117, 159, 6948])
    CharStartOutfit(race=c.Race.TROLL, class_=c.Class.SHAMAN, gender=c.Gender.FEMALE, equipment=[{'entry': 36, 'equipment_slot': 'MAIN_HAND'}, {'entry': 6134, 'equipment_slot': 'BODY'}, {'entry': 6135, 'equipment_slot': 'LEGS'}], items=[117, 159, 6948])
    CharStartOutfit(race=c.Race.TROLL, class_=c.Class.MAGE, gender=c.Gender.MALE, equipment=[{'entry': 6140, 'equipment_slot': 'CHEST'}, {'entry': 1395, 'equipment_slot': 'LEGS'}, {'entry': 6096, 'equipment_slot': 'BODY'}, {'entry': 55, 'equipment_slot': 'FEET'}, {'entry': 35, 'equipment_slot': 'MAIN_HAND'}], items=[117, 159, 6948])
    CharStartOutfit(race=c.Race.TROLL, class_=c.Class.MAGE, gender=c.Gender.FEMALE, equipment=[{'entry': 6140, 'equipment_slot': 'CHEST'}, {'entry': 1395, 'equipment_slot': 'LEGS'}, {'entry': 6096, 'equipment_slot': 'BODY'}, {'entry': 55, 'equipment_slot': 'FEET'}, {'entry': 35, 'equipment_slot': 'MAIN_HAND'}], items=[117, 159, 6948])


    logging.info('Loading UnitTemplate...')
    with gzip.GzipFile('database/dbc/unit_template.json.gz') as f:
        for unit_template in json.load(f):
            UnitTemplate(**unit_template)

    logging.info('Loading ItemTemplate...')
    with gzip.GzipFile('database/dbc/item_template.json.gz') as f:
        for item_template in json.load(f):
            ItemTemplate(**item_template)

    # yapf: enable
