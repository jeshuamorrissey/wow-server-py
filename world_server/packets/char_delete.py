from construct import Int8ul, Int32ul, Struct

from world_server import op_code, router

ClientCharDelete = router.ClientPacket.Register(
    op_code.Client.CHAR_DELETE,
    Struct(
        'guid_low' / Int32ul,
        'guid_high' / Int32ul,
    ),
)

ServerCharDelete = Struct('error' / Int8ul)
