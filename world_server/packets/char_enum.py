from construct import (Array, BitStruct, Const, CString, Default, Flag,
                       Float32l, GreedyRange, Int8ul, Int32ul, Int64ul,
                       Padding, Rebuild, Struct)

from world_server import op_code, router

ClientCharEnum = router.ClientPacket.Register(
    op_code.Client.CHAR_ENUM,
    Struct(),
)

ServerCharEnum = Struct(
    'num_characters' / Rebuild(Int8ul, lambda this: len(this.characters)),
    'characters' / GreedyRange(
        Struct(
            'guid' / Int64ul,
            'name' / CString('ascii'),
            'race' / Int8ul,
            'class_' / Int8ul,
            'gender' / Int8ul,
            'appearance' / Struct(
                'skin' / Int8ul,
                'face' / Int8ul,
                'hair_style' / Int8ul,
                'hair_color' / Int8ul,
                'feature' / Int8ul,
            ),
            'level' / Int8ul,
            'location' / Struct(
                'zone' / Int32ul,
                'map' / Int32ul,
                'x' / Float32l,
                'y' / Float32l,
                'z' / Float32l,
            ),
            'guild_id' / Int32ul,
            'flags' / BitStruct(
                Padding(10),
                'is_ghost' / Flag,
                Padding(1),
                'hide_helm' / Flag,
                'hide_cloak' / Flag,
                Padding(18),
            ),
            Const(b'\x00'),  # first login?
            'pet' / Struct(
                'id' / Int32ul,
                'level' / Int32ul,
                'family' / Int32ul,
            ),
            'items' / Struct(
                'display_id' / Default(Int32ul, 0),
                'inventory_type' / Default(Int8ul, 0),
            )[19],
            'first_bag' / Struct(
                'display_id' / Int32ul,
                'inventory_type' / Int8ul,
            ),
        )))
