from construct import Struct, Rebuild, Int8ul, Int64ul, Flag, Padding, CString, Int32ul, Float32l, GreedyRange, Array, BitStruct

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
                Padding(21),
            ),
            'first_login' / Int8ul,
            'pet' / Struct(
                'id' / Int32ul,
                'level' / Int32ul,
                'family' / Int32ul,
            ),
            'items' / Struct(
                'display_id' / Int32ul,
                'inventory_type' / Int8ul,
            )[19],
            'first_bag' / Struct(
                'display_id' / Int32ul,
                'inventory_type' / Int8ul,
            ),
        )))
