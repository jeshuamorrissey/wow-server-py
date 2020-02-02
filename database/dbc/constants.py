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
