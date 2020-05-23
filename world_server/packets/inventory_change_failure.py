from typing import List, Tuple

from construct import Default, If, Int8ul, Int32ul, Int64ul, Struct

from database import enums
from world_server import op_code

ServerInventoryChangeFailure = Struct(
    'code' / Int8ul,
    'result' / If(
        lambda c: c.code != enums.InventoryChangeError.OK,
        Struct(
            'required_level' /
            If(lambda c: c._.code == enums.InventoryChangeError.CANT_EQUIP_LEVEL_I, Default(Int32ul, 0)),
            'item1_guid' / Default(Int64ul, 0),
            'item2_guid' / Default(Int64ul, 0),
            'bag_subclass' / Default(Int8ul, 0),
        ),
    ),
)


def error(code: enums.InventoryChangeError, **kwargs) -> List[Tuple[op_code.Server, bytes]]:
    return [(
        op_code.Server.INVENTORY_CHANGE_FAILURE,
        ServerInventoryChangeFailure.build(dict(
            code=code,
            result=dict(**kwargs),
        )),
    )]
