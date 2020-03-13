from construct import (Array, Const, Enum, GreedyRange, Int8ul, Int16ul, Int24ul, Int32ul, Padding, Rebuild, Struct)

from database import enums

ServerActionButtons = Struct(
    'actions' / Array(120, Struct(
        'action' / Int24ul,
        'type' / Enum(Int8ul, enums.ActionButtonType),
    )),)
