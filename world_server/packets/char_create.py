from construct import CString, Int8ul, Struct

from world_server import op_code, router

ClientCharCreate = router.ClientPacket.Register(
    op_code.Client.CHAR_CREATE,
    Struct(
        'name' / CString('ascii'),
        'race' / Int8ul,
        'class_' / Int8ul,
        'gender' / Int8ul,
        'skin_color' / Int8ul,
        'face' / Int8ul,
        'hair_style' / Int8ul,
        'hair_color' / Int8ul,
        'feature' / Int8ul,
        'outfit_id' / Int8ul,
    ),
)

ServerCharCreate = Struct('error' / Int8ul)
