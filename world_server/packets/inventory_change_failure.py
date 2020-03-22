import enum
from typing import List, Tuple

from construct import Default, Enum, If, Int8ul, Int32ul, Int64ul, Struct

from world_server import op_code


class ErrorCode(enum.IntEnum):
    OK = 0
    CANT_EQUIP_LEVEL_I = 1
    CANT_EQUIP_SKILL = 2
    ITEM_DOESNT_GO_TO_SLOT = 3
    BAG_FULL = 4
    NONEMPTY_BAG_OVER_OTHER_BAG = 5
    CANT_TRADE_EQUIP_BAGS = 6
    ONLY_AMMO_CAN_GO_HERE = 7
    NO_REQUIRED_PROFICIENCY = 8
    NO_EQUIPMENT_SLOT_AVAILABLE = 9
    YOU_CAN_NEVER_USE_THAT_ITEM = 10
    YOU_CAN_NEVER_USE_THAT_ITEM2 = 11
    NO_EQUIPMENT_SLOT_AVAILABLE2 = 12
    CANT_EQUIP_WITH_TWOHANDED = 13
    CANT_DUAL_WIELD = 14
    ITEM_DOESNT_GO_INTO_BAG = 15
    ITEM_DOESNT_GO_INTO_BAG2 = 16
    CANT_CARRY_MORE_OF_THIS = 17
    NO_EQUIPMENT_SLOT_AVAILABLE3 = 18
    ITEM_CANT_STACK = 19
    ITEM_CANT_BE_EQUIPPED = 20
    ITEMS_CANT_BE_SWAPPED = 21
    SLOT_IS_EMPTY = 22
    ITEM_NOT_FOUND = 23
    CANT_DROP_SOULBOUND = 24
    OUT_OF_RANGE = 25
    TRIED_TO_SPLIT_MORE_THAN_COUNT = 26
    COULDNT_SPLIT_ITEMS = 27
    MISSING_REAGENT = 28
    NOT_ENOUGH_MONEY = 29
    NOT_A_BAG = 30
    CAN_ONLY_DO_WITH_EMPTY_BAGS = 31
    DONT_OWN_THAT_ITEM = 32
    CAN_EQUIP_ONLY1_QUIVER = 33
    MUST_PURCHASE_THAT_BAG_SLOT = 34
    TOO_FAR_AWAY_FROM_BANK = 35
    ITEM_LOCKED = 36
    YOU_ARE_STUNNED = 37
    YOU_ARE_DEAD = 38
    CANT_DO_RIGHT_NOW = 39
    INT_BAG_ERROR = 40
    CAN_EQUIP_ONLY1_BOLT = 41
    CAN_EQUIP_ONLY1_AMMOPOUCH = 42
    STACKABLE_CANT_BE_WRAPPED = 43
    EQUIPPED_CANT_BE_WRAPPED = 44
    WRAPPED_CANT_BE_WRAPPED = 45
    BOUND_CANT_BE_WRAPPED = 46
    UNIQUE_CANT_BE_WRAPPED = 47
    BAGS_CANT_BE_WRAPPED = 48
    ALREADY_LOOTED = 49
    INVENTORY_FULL = 50
    BANK_FULL = 51
    ITEM_IS_CURRENTLY_SOLD_OUT = 52
    BAG_FULL3 = 53
    ITEM_NOT_FOUND2 = 54
    ITEM_CANT_STACK2 = 55
    BAG_FULL4 = 56
    ITEM_SOLD_OUT = 57
    OBJECT_IS_BUSY = 58
    NONE = 59
    NOT_IN_COMBAT = 60
    NOT_WHILE_DISARMED = 61
    BAG_FULL6 = 62
    CANT_EQUIP_RANK = 63
    CANT_EQUIP_REPUTATION = 64
    TOO_MANY_SPECIAL_BAGS = 65
    LOOT_CANT_LOOT_THAT_NOW = 66


ServerInventoryChangeFailure = Struct(
    'code' / Enum(Int8ul, ErrorCode),
    'result' / If(
        lambda c: c.code != ErrorCode.OK,
        Struct(
            'required_level' / If(lambda c: c._.code == ErrorCode.CANT_EQUIP_LEVEL_I, Int32ul),
            'item1_guid' / Default(Int64ul, 0),
            'item2_guid' / Default(Int64ul, 0),
            'bag_subclass' / Default(Int8ul, 0),
        ),
    ),
)


def error(code: ErrorCode, **kwargs) -> List[Tuple[op_code.Server, bytes]]:
    return [(
        op_code.Server.INVENTORY_CHANGE_FAILURE,
        ServerInventoryChangeFailure.build(dict(
            code=code,
            result=dict(**kwargs),
        )),
    )]
