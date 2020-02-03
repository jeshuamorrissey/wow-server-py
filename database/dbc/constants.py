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


class UpdateType(enum.IntEnum):
    VALUES = 0
    MOVEMENT = 1
    CREATE_OBJECT = 2
    CREATE_OBJECT2 = 3
    OUT_OF_RANGE_OBJECTS = 4
    NEAR_OBJECTS = 5


class TypeID(enum.IntEnum):
    OBJECT = 0
    ITEM = 1
    CONTAINER = 2
    UNIT = 3
    PLAYER = 4
    GAMEOBJECT = 5
    DYNAMICOBJECT = 6
    CORPSE = 7


class UpdateFlags(enum.IntFlag):
    NONE = 0x0000
    SELF = 0x0001
    TRANSPORT = 0x0002
    FULLGUID = 0x0004
    HIGHGUID = 0x0008
    ALL = 0x0010
    LIVING = 0x0020
    HAS_POSITION = 0x0040


class MovementFlags(enum.IntFlag):
    NONE = 0x00000000
    FORWARD = 0x00000001
    BACKWARD = 0x00000002
    STRAFE_LEFT = 0x00000004
    STRAFE_RIGHT = 0x00000008
    TURN_LEFT = 0x00000010
    TURN_RIGHT = 0x00000020
    PITCH_UP = 0x00000040
    PITCH_DOWN = 0x00000080
    WALK_MODE = 0x00000100
    LEVITATING = 0x00000400
    FLYING = 0x00000800
    FALLING = 0x00002000
    FALLINGFAR = 0x00004000
    SWIMMING = 0x00200000
    SPLINE_ENABLED = 0x00400000
    CAN_FLY = 0x00800000
    FLYING_OLD = 0x01000000
    ONTRANSPORT = 0x02000000
    SPLINE_ELEVATION = 0x04000000
    ROOT = 0x08000000
    WATERWALKING = 0x10000000
    SAFE_FALL = 0x20000000
    HOVER = 0x40000000


class SplineFlags(enum.IntFlag):
    NoFlags = 0x00000000
    Done = 0x00000001
    Falling = 0x00000002
    Unknown3 = 0x00000004
    Unknown4 = 0x00000008
    Unknown5 = 0x00000010
    Unknown6 = 0x00000020
    Unknown7 = 0x00000040
    Unknown8 = 0x00000080
    Runmode = 0x00000100
    Flying = 0x00000200
    No_Spline = 0x00000400
    Unknown12 = 0x00000800
    Unknown13 = 0x00001000
    Unknown14 = 0x00002000
    Unknown15 = 0x00004000
    Unknown16 = 0x00008000
    Final_Point = 0x00010000
    Final_Target = 0x00020000
    Final_Angle = 0x00040000
    Unknown19 = 0x00080000
    Cyclic = 0x00100000
    Enter_Cycle = 0x00200000
    Frozen = 0x00400000
    Unknown23 = 0x00800000
    Unknown24 = 0x01000000
    Unknown25 = 0x02000000
    Unknown26 = 0x04000000
    Unknown27 = 0x08000000
    Unknown28 = 0x10000000
    Unknown29 = 0x20000000
    Unknown30 = 0x40000000
    Unknown31 = 0x80000000

    Mask_Final_Facing = Final_Point | Final_Target | Final_Angle
    Mask_No_Monster_Move = Mask_Final_Facing | Done
    Mask_CatmullRom = Flying


class TypeMask(enum.IntFlag):
    OBJECT = 0x0001
    ITEM = 0x0002
    CONTAINER = 0x0004
    UNIT = 0x0008
    PLAYER = 0x0010
    GAMEOBJECT = 0x0020
    DYNAMICOBJECT = 0x0040
    CORPSE = 0x0080


class HighGUID(enum.IntEnum):
    ITEM = 0x40000000
    CONTAINER = 0x40000000
    PLAYER = 0x00000000
    GAMEOBJECT = 0xF1100000
    TRANSPORT = 0xF1200000
    UNIT = 0xF1300000
    PET = 0xF1400000
    DYNAMICOBJECT = 0xF1000000
    CORPSE = 0xF1010000
    MO_TRANSPORT = 0x1FC00000
