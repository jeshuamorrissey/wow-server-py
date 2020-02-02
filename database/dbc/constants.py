"""DBC constants, easier than reading them from the raw DBC files."""
import enum


class Gender(enum.IntEnum):
    MALE = 0
    FEMALE = 1


class Race(enum.IntEnum):
    HUMAN = 1
    ORC = 2
    DWARF = 3
    NIGHTELF = 4
    UNDEAD = 5
    TAUREN = 6
    GNOME = 7
    TROLL = 8
    GOBLIN = 9


class Class(enum.IntEnum):
    WARRIOR = 1
    PALADIN = 2
    HUNTER = 3
    ROGUE = 4
    PRIEST = 5
    SHAMAN = 7
    MAGE = 8
    WARLOCK = 9
    DRUID = 11


class EquipmentSlot(enum.IntEnum):
    HEAD = 0
    NECK = 1
    SHOULDERS = 2
    BODY = 3
    CHEST = 4
    WAIST = 5
    LEGS = 6
    FEET = 7
    WRISTS = 8
    HANDS = 9
    FINGER1 = 10
    FINGER2 = 11
    TRINKET1 = 12
    TRINKET2 = 13
    BACK = 14
    MAIN_HAND = 15
    OFF_HAND = 16
    RANGED = 17
    TABARD = 18
