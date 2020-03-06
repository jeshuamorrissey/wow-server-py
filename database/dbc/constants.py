"""DBC constants, easier than reading them from the raw DBC files."""
import enum


class Gender(enum.IntEnum):
    MALE = 0
    FEMALE = 1


def NextLevelXP(level: int) -> int:
    assert level > 0

    return 10000  # TODO: exp formula


def MaxNumberOfProfessions() -> int:
    return 10  # TODO: make this config


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


class Team(enum.IntEnum):
    HORDE = 67
    ALLIANCE = 469


class SheathedState(enum.IntEnum):
    UNARMED = 0
    MELEE = 1
    RANGED = 2


class StandState(enum.IntEnum):
    STAND = 0
    SIT = 1
    SIT_CHAIR = 2
    SLEEP = 3
    SIT_LOW_CHAIR = 4
    SIT_MEDIUM_CHAIR = 5
    SIT_HIGH_CHAIR = 6
    DEAD = 7
    KNEEL = 8


class EnchantmentSlot(enum.IntEnum):
    PERMANENT = 0
    TEMPORARY = 1
    PROPERTY_0 = 3
    PROPERTY_1 = 4
    PROPERTY_2 = 5
    PROPERTY_3 = 6


class QuestStatus(enum.IntEnum):
    NONE = 0
    COMPLETE = 1
    UNAVAILABLE = 2
    INCOMPLETE = 3
    AVAILABLE = 4
    FAILED = 5
    FORCE_COMPLETE = 6


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


class AuraState(enum.IntFlag):
    NONE = 0
    DEFENSE = 1 << 0
    HEALTHLESS_20_PERCENT = 1 << 1
    BERSERKING = 1 << 2
    FROZEN = 1 << 3
    JUDGEMENT = 1 << 4
    HUNTER_PARRY = 1 << 6
    ROGUE_ATTACK_FROM_STEALTH = 1 << 6


class Stat(enum.IntEnum):
    STRENGTH = 0
    AGILITY = 1
    STAMINA = 2
    INTELLECT = 3
    SPIRIT = 4


class SpellSchool(enum.IntEnum):
    NORMAL = 0
    HOLY = 1
    FIRE = 2
    NATURE = 3
    FROST = 4
    SHADOW = 5
    ARCANE = 6


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


class PowerType(enum.IntEnum):
    MANA = 0
    RAGE = 1
    FOCUS = 2
    ENERGY = 3
    HAPPINESS = 4


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
    ITEM = 0x4000
    CONTAINER = 0x4000
    PLAYER = 0x0000
    GAMEOBJECT = 0xF110
    TRANSPORT = 0xF120
    UNIT = 0xF130
    PET = 0xF140
    DYNAMICOBJECT = 0xF100
    CORPSE = 0xF101
    MO_TRANSPORT = 0x1FC0


class UpdateField(enum.IntEnum):
    pass


class ObjectFields(UpdateField):
    GUID = 0x00
    TYPE = 0x02
    ENTRY = 0x03
    SCALE_X = 0x04
    PADDING = 0x05
    END = 0x06


class ItemFields(UpdateField):
    OWNER = ObjectFields.END + 0x00
    CONTAINED = ObjectFields.END + 0x02
    CREATOR = ObjectFields.END + 0x04
    GIFTCREATOR = ObjectFields.END + 0x06
    STACK_COUNT = ObjectFields.END + 0x08
    DURATION = ObjectFields.END + 0x09
    SPELL_CHARGES = ObjectFields.END + 0x0A
    SPELL_CHARGES_01 = ObjectFields.END + 0x0B
    SPELL_CHARGES_02 = ObjectFields.END + 0x0C
    SPELL_CHARGES_03 = ObjectFields.END + 0x0D
    SPELL_CHARGES_04 = ObjectFields.END + 0x0E
    FLAGS = ObjectFields.END + 0x0F
    ENCHANTMENT = ObjectFields.END + 0x10
    PROPERTY_SEED = ObjectFields.END + 0x25
    RANDOM_PROPERTIES_ID = ObjectFields.END + 0x26
    ITEM_TEXT_ID = ObjectFields.END + 0x27
    DURABILITY = ObjectFields.END + 0x28
    MAXDURABILITY = ObjectFields.END + 0x29
    END = ObjectFields.END + 0x2A


class ContainerFields(UpdateField):
    NUM_SLOTS = ItemFields.END + 0x00
    ALIGN_PAD = ItemFields.END + 0x01
    SLOT_1 = ItemFields.END + 0x02
    SLOT_LAST = ItemFields.END + 0x38
    END = ItemFields.END + 0x3A


class UnitFields(UpdateField):
    CHARM = ObjectFields.END + 0x00
    SUMMON = ObjectFields.END + 0x02
    CHARMEDBY = ObjectFields.END + 0x04
    SUMMONEDBY = ObjectFields.END + 0x06
    CREATEDBY = ObjectFields.END + 0x08
    TARGET = ObjectFields.END + 0x0A
    PERSUADED = ObjectFields.END + 0x0C
    CHANNEL = ObjectFields.END + 0x0E
    HEALTH = ObjectFields.END + 0x10
    POWER_START = ObjectFields.END + 0x11  # power = POWER_START + c.PowerType
    MAXHEALTH = ObjectFields.END + 0x16
    MAX_POWER_START = ObjectFields.END + 0x17  # max_power = MAX_POWER_START + c.PowerType
    LEVEL = ObjectFields.END + 0x1C
    FACTIONTEMPLATE = ObjectFields.END + 0x1D
    BYTES_0 = ObjectFields.END + 0x1E

    # Information about which items are currently being displayed.
    # This is for sheathing/unsheating weapons. These fields encode:
    #
    #     - DISPLAY = The display ID of the item.
    #     - INFO_0[0] = Item Class
    #     - INFO_0[1] = Item Subclass
    #     - INFO_0[2] = Item Material
    #     - INFO_0[3] = Item Inventory Type
    #     - INFO_1[0] = Sheath
    #
    MAIN_HAND_DISPLAY = ObjectFields.END + 0x1F
    OFF_HAND_DISPLAY = ObjectFields.END + 0x20
    RANGED_DISPLAY = ObjectFields.END + 0x21
    MAIN_HAND_INFO_0 = ObjectFields.END + 0x22
    MAIN_HAND_INFO_1 = ObjectFields.END + 0x23
    OFF_HAND_INFO_0 = ObjectFields.END + 0x24
    OFF_HAND_INFO_1 = ObjectFields.END + 0x25
    RANGED_INFO_0 = ObjectFields.END + 0x26
    RANGED_INFO_1 = ObjectFields.END + 0x27

    FLAGS = ObjectFields.END + 0x28

    ##
    ## Aura Fields
    ##
    # 48 fields, each containing the spell ID of an aura.
    AURA = ObjectFields.END + 0x29

    # 48 half-bytes (6 fields) of flags, not sure why this is needed.
    AURAFLAGS = ObjectFields.END + 0x59

    # 48 bytes (12 fields) specifying the level of the unit that cast
    # the aura.
    AURALEVELS = ObjectFields.END + 0x5f

    # 48 bytes (12 fields) specifying the number of applications of each
    # aura.
    AURAAPPLICATIONS = ObjectFields.END + 0x6b

    # State byte deciding what the character looks like, usually applied
    # by their auras.
    AURASTATE = ObjectFields.END + 0x77
    ##
    ## END Aura Fields
    ##

    BASEATTACKTIME = ObjectFields.END + 0x78
    OFFHANDATTACKTIME = ObjectFields.END + 0x79
    RANGEDATTACKTIME = ObjectFields.END + 0x7a
    BOUNDINGRADIUS = ObjectFields.END + 0x7b
    COMBATREACH = ObjectFields.END + 0x7c
    DISPLAYID = ObjectFields.END + 0x7d
    NATIVEDISPLAYID = ObjectFields.END + 0x7e
    MOUNTDISPLAYID = ObjectFields.END + 0x7f
    MINDAMAGE = ObjectFields.END + 0x80
    MAXDAMAGE = ObjectFields.END + 0x81
    MINOFFHANDDAMAGE = ObjectFields.END + 0x82
    MAXOFFHANDDAMAGE = ObjectFields.END + 0x83
    BYTES_1 = ObjectFields.END + 0x84
    PETNUMBER = ObjectFields.END + 0x85
    PET_NAME_TIMESTAMP = ObjectFields.END + 0x86
    PETEXPERIENCE = ObjectFields.END + 0x87
    PETNEXTLEVELEXP = ObjectFields.END + 0x88
    DYNAMIC_FLAGS = ObjectFields.END + 0x89
    CHANNEL_SPELL = ObjectFields.END + 0x8a
    MOD_CAST_SPEED = ObjectFields.END + 0x8b
    CREATED_BY_SPELL = ObjectFields.END + 0x8c
    NPC_FLAGS = ObjectFields.END + 0x8d
    NPC_EMOTESTATE = ObjectFields.END + 0x8e
    TRAINING_POINTS = ObjectFields.END + 0x8f
    STRENGTH = ObjectFields.END + 0x90
    AGILITY = ObjectFields.END + 0x91
    STAMINA = ObjectFields.END + 0x92
    INTELLECT = ObjectFields.END + 0x93
    SPIRIT = ObjectFields.END + 0x94
    ARMOR = ObjectFields.END + 0x95
    HOLY_RESISTANCE = ObjectFields.END + 0x96
    FIRE_RESISTANCE = ObjectFields.END + 0x97
    NATURE_RESISTANCE = ObjectFields.END + 0x98
    FROST_RESISTANCE = ObjectFields.END + 0x99
    SHADOW_RESISTANCE = ObjectFields.END + 0x9a
    ARCANE_RESISTANCE = ObjectFields.END + 0x9b
    BASE_MANA = ObjectFields.END + 0x9c
    BASE_HEALTH = ObjectFields.END + 0x9d
    BYTES_2 = ObjectFields.END + 0x9e
    ATTACK_POWER = ObjectFields.END + 0x9f
    ATTACK_POWER_MODS = ObjectFields.END + 0xa0
    ATTACK_POWER_MULTIPLIER = ObjectFields.END + 0xa1
    RANGED_ATTACK_POWER = ObjectFields.END + 0xa2
    RANGED_ATTACK_POWER_MODS = ObjectFields.END + 0xa3
    RANGED_ATTACK_POWER_MULTIPLIER = ObjectFields.END + 0xa4
    MINRANGEDDAMAGE = ObjectFields.END + 0xa5
    MAXRANGEDDAMAGE = ObjectFields.END + 0xa6
    POWER_COST_MODIFIER = ObjectFields.END + 0xa7
    POWER_COST_MULTIPLIER = ObjectFields.END + 0xae
    PADDING = ObjectFields.END + 0xb5
    END = ObjectFields.END + 0xb6


class PlayerFields(UpdateField):
    DUEL_ARBITER = UnitFields.END + 0x00
    FLAGS = UnitFields.END + 0x02
    GUILDID = UnitFields.END + 0x03
    GUILDRANK = UnitFields.END + 0x04
    BYTES = UnitFields.END + 0x05
    BYTES_2 = UnitFields.END + 0x06
    BYTES_3 = UnitFields.END + 0x07
    DUEL_TEAM = UnitFields.END + 0x08
    GUILD_TIMESTAMP = UnitFields.END + 0x09

    # Three fields per quest:
    #     - ID: The quests ID
    #     - Flags[0-2]: 6 bits per quest objective count (yes, really)
    #     - Flags[3]: QuestState
    #     - Timer: The quests timer
    QUEST_LOG_1_1 = UnitFields.END + 0x0A
    QUEST_LOG_1_2 = UnitFields.END + 0x0B
    QUEST_LOG_1_3 = UnitFields.END + 0x0C
    QUEST_LOG_LAST_1 = UnitFields.END + 0x43
    QUEST_LOG_LAST_2 = UnitFields.END + 0x44
    QUEST_LOG_LAST_3 = UnitFields.END + 0x45

    # Define information about which items are visible on the character.
    # This includes one item per slot, with the following 12 sub-fields:
    #     - CREATOR[2]: The GUID of the Player which created this item (or 0)
    #     - ENTRY[1]: The item's entry
    #     - ENCHANTMENT[7]: The enchantment IDs (see c.EnchantmentSlot)
    #     - RANDOM_PROPERTY[1]: The item's random property ID
    #     - SUFFIX_FACTOR[1]: The item's suffix factor
    VISIBLE_ITEM_START = UnitFields.END + 0x46

    # Define which items are in the player's inventory. This includes all
    # equipped items, with a GUID for each equipment slot.
    INVENTORY_START = UnitFields.END + 0x12a

    BAG_SLOT_1 = UnitFields.END + 0x150
    BAG_SLOT_LAST = UnitFields.END + 0x156
    PACK_SLOT_1 = UnitFields.END + 0x158
    PACK_SLOT_LAST = UnitFields.END + 0x176
    BANK_SLOT_1 = UnitFields.END + 0x178
    BANK_SLOT_LAST = UnitFields.END + 0x1a6
    BANKBAG_SLOT_1 = UnitFields.END + 0x1a8
    BANKBAG_SLOT_LAST = UnitFields.END + 0x1b2
    VENDORBUYBACK_SLOT_1 = UnitFields.END + 0x1b4
    VENDORBUYBACK_SLOT_LAST = UnitFields.END + 0x1ca
    KEYRING_SLOT_1 = UnitFields.END + 0x1cc
    KEYRING_SLOT_LAST = UnitFields.END + 0x20a
    FARSIGHT = UnitFields.END + 0x20c
    COMBO_TARGET = UnitFields.END + 0x20e
    XP = UnitFields.END + 0x210
    NEXT_LEVEL_XP = UnitFields.END + 0x211
    SKILL_INFO_1_1 = UnitFields.END + 0x212
    CHARACTER_POINTS1 = UnitFields.END + 0x392
    CHARACTER_POINTS2 = UnitFields.END + 0x393
    TRACK_CREATURES = UnitFields.END + 0x394
    TRACK_RESOURCES = UnitFields.END + 0x395
    BLOCK_PERCENTAGE = UnitFields.END + 0x396
    DODGE_PERCENTAGE = UnitFields.END + 0x397
    PARRY_PERCENTAGE = UnitFields.END + 0x398
    CRIT_PERCENTAGE = UnitFields.END + 0x399
    RANGED_CRIT_PERCENTAGE = UnitFields.END + 0x39a
    EXPLORED_ZONES_1 = UnitFields.END + 0x39b
    REST_STATE_EXPERIENCE = UnitFields.END + 0x3db
    COINAGE = UnitFields.END + 0x3dc
    POSSTAT0 = UnitFields.END + 0x3DD
    POSSTAT1 = UnitFields.END + 0x3DE
    POSSTAT2 = UnitFields.END + 0x3DF
    POSSTAT3 = UnitFields.END + 0x3E0
    POSSTAT4 = UnitFields.END + 0x3E1
    NEGSTAT0 = UnitFields.END + 0x3E2
    NEGSTAT1 = UnitFields.END + 0x3E3
    NEGSTAT2 = UnitFields.END + 0x3E4
    NEGSTAT3 = UnitFields.END + 0x3E5
    NEGSTAT4 = UnitFields.END + 0x3E6
    RESISTANCEBUFFMODSPOSITIVE = UnitFields.END + 0x3E7
    RESISTANCEBUFFMODSNEGATIVE = UnitFields.END + 0x3EE
    MOD_DAMAGE_DONE_POS = UnitFields.END + 0x3F5
    MOD_DAMAGE_DONE_NEG = UnitFields.END + 0x3FC
    MOD_DAMAGE_DONE_PCT = UnitFields.END + 0x403
    BYTES_4 = UnitFields.END + 0x40A
    AMMO_ID = UnitFields.END + 0x40B
    SELF_RES_SPELL = UnitFields.END + 0x40C
    PVP_MEDALS = UnitFields.END + 0x40D
    BUYBACK_PRICE_1 = UnitFields.END + 0x40E
    BUYBACK_PRICE_LAST = UnitFields.END + 0x419
    BUYBACK_TIMESTAMP_1 = UnitFields.END + 0x41A
    BUYBACK_TIMESTAMP_LAST = UnitFields.END + 0x425
    SESSION_KILLS = UnitFields.END + 0x426
    YESTERDAY_KILLS = UnitFields.END + 0x427
    LAST_WEEK_KILLS = UnitFields.END + 0x428
    THIS_WEEK_KILLS = UnitFields.END + 0x429
    THIS_WEEK_CONTRIBUTION = UnitFields.END + 0x42a
    LIFETIME_HONORABLE_KILLS = UnitFields.END + 0x42b
    LIFETIME_DISHONORABLE_KILLS = UnitFields.END + 0x42c
    YESTERDAY_CONTRIBUTION = UnitFields.END + 0x42d
    LAST_WEEK_CONTRIBUTION = UnitFields.END + 0x42e
    LAST_WEEK_RANK = UnitFields.END + 0x42f
    BYTES2 = UnitFields.END + 0x430
    WATCHED_FACTION_INDEX = UnitFields.END + 0x431
    COMBAT_RATING_1 = UnitFields.END + 0x432
    END = UnitFields.END + 0x446


class GameObjectFields(UpdateField):
    CREATED_BY = ObjectFields.END + 0x00
    DISPLAYID = ObjectFields.END + 0x02
    FLAGS = ObjectFields.END + 0x03
    ROTATION = ObjectFields.END + 0x04
    STATE = ObjectFields.END + 0x08
    POS_X = ObjectFields.END + 0x09
    POS_Y = ObjectFields.END + 0x0A
    POS_Z = ObjectFields.END + 0x0B
    FACING = ObjectFields.END + 0x0C
    DYN_FLAGS = ObjectFields.END + 0x0D
    FACTION = ObjectFields.END + 0x0E
    TYPE_ID = ObjectFields.END + 0x0F
    LEVEL = ObjectFields.END + 0x10
    ARTKIT = ObjectFields.END + 0x11
    ANIMPROGRESS = ObjectFields.END + 0x12
    PADDING = ObjectFields.END + 0x13
    END = ObjectFields.END + 0x14


class DynamicObjectFields(UpdateField):
    CASTER = ObjectFields.END + 0x00
    BYTES = ObjectFields.END + 0x02
    SPELLID = ObjectFields.END + 0x03
    RADIUS = ObjectFields.END + 0x04
    POS_X = ObjectFields.END + 0x05
    POS_Y = ObjectFields.END + 0x06
    POS_Z = ObjectFields.END + 0x07
    FACING = ObjectFields.END + 0x08
    PAD = ObjectFields.END + 0x09
    END = ObjectFields.END + 0x0A


class CorpseFields(enum.IntEnum):
    OWNER = ObjectFields.END + 0x00
    FACING = ObjectFields.END + 0x02
    POS_X = ObjectFields.END + 0x03
    POS_Y = ObjectFields.END + 0x04
    POS_Z = ObjectFields.END + 0x05
    DISPLAY_ID = ObjectFields.END + 0x06
    ITEM = ObjectFields.END + 0x07
    BYTES_1 = ObjectFields.END + 0x1A
    BYTES_2 = ObjectFields.END + 0x1B
    GUILD = ObjectFields.END + 0x1C
    FLAGS = ObjectFields.END + 0x1D
    DYNAMIC_FLAGS = ObjectFields.END + 0x1E
    PAD = ObjectFields.END + 0x1F
    END = ObjectFields.END + 0x20


class ItemFlags(enum.IntFlag):
    BOUND = 0x00000001
    UNLOCKED = 0x00000004
    WRAPPED = 0x00000008
    READABLE = 0x00000200


class PlayerFlags(enum.IntFlag):
    NONE = 0x00000000
    GROUP_LEADER = 0x00000001
    AFK = 0x00000002
    DND = 0x00000004
    GM = 0x00000008
    GHOST = 0x00000010
    RESTING = 0x00000020
    UNK7 = 0x00000040
    FFA_PVP = 0x00000080
    CONTESTED_PVP = 0x00000100
    IN_PVP = 0x00000200
    HIDE_HELM = 0x00000400
    HIDE_CLOAK = 0x00000800
    PARTIAL_PLAY_TIME = 0x00001000
    NO_PLAY_TIME = 0x00002000
    UNK15 = 0x00004000
    UNK16 = 0x00008000
    SANCTUARY = 0x00010000
    TAXI_BENCHMARK = 0x00020000
    PVP_TIMER = 0x00040000


class UnitFlags(enum.IntFlag):
    NONE = 0x00000000
    NON_ATTACKABLE = 0x00000002
    DISABLE_MOVE = 0x00000004
    PVP_ATTACKABLE = 0x00000008
    RENAME = 0x00000010
    RESTING = 0x00000020
    OOC_NOT_ATTACKABLE = 0x00000100
    PASSIVE = 0x00000200
    PVP = 0x00001000
    SILENCED = 0x00002000
    PACIFIED = 0x00020000
    DISABLE_ROTATE = 0x00040000
    IN_COMBAT = 0x00080000
    NOT_SELECTABLE = 0x02000000
    SKINNABLE = 0x04000000
    AURAS_VISIBLE = 0x08000000
    SHEATHE = 0x40000000
    NOT_ATTACKABLE_1 = 0x00000080
    LOOTING = 0x00000400
    PET_IN_COMBAT = 0x00000800
    STUNNED = 0x00040000
    TAXI_FLIGHT = 0x00100000
    DISARMED = 0x00200000
    CONFUSED = 0x00400000
    FLEEING = 0x00800000
    PLAYER_CONTROLLED = 0x01000000


class UnitBytes1Flags(enum.IntFlag):
    ALWAYS_STAND = 0x01
    CREEP = 0x02
    UNTRACKABLE = 0x04
    ALL = 0xFF


class UnitDynamicFlags(enum.IntFlag):
    NONE = 0x0000
    LOOTABLE = 0x0001
    TRACK_UNIT = 0x0002
    TAPPED = 0x0004
    ROOTED = 0x0008
    SPECIALINFO = 0x0010
    DEAD = 0x0020


class PlayerByteFlags(enum.IntFlag):
    TRACK_STEALTHED = 0x02
    RELEASE_TIMER = 0x08
    NO_RELEASE_WINDOW = 0x10


class PlayerByte2Flags(enum.IntFlag):
    NONE = 0x00
    DETECT_AMORE_0 = 0x02
    DETECT_AMORE_1 = 0x04
    DETECT_AMORE_2 = 0x08
    DETECT_AMORE_3 = 0x10
    STEALTH = 0x20
    INVISIBILITY_GLOW = 0x40
