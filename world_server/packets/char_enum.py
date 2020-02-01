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
            'flags' / BitStruct(  # TODO: what do these flags actually do?
                'f0' / Flag,
                'f1' / Flag,
                'f2' / Flag,
                'f3' / Flag,
                'f4' / Flag,
                'f5' / Flag,
                'f6' / Flag,
                'f7' / Flag,
                'f8' / Flag,
                'f9' / Flag,
                'f10' / Flag,
                'f11' / Flag,
                'f12' / Flag,
                'f13' / Flag,
                'f14' / Flag,
                'f15' / Flag,
                'f16' / Flag,
                'f17' / Flag,
                'f18' / Flag,
                'f19' / Flag,
                'f20' / Flag,
                'f21' / Flag,
                'f22' / Flag,
                'f23' / Flag,
                'f24' / Flag,
                'f25' / Flag,
                'f26' / Flag,
                'f27' / Flag,
                'f28' / Flag,
                'f29' / Flag,
                'f30' / Flag,
                'f31' / Flag,
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
