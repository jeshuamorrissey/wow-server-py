from construct import Int32ul, Struct

from world_server import op_code, router

ClientPlayerLogin = router.ClientPacket.Register(
    op_code.Client.PLAYER_LOGIN,
    Struct(
        'guid_low' / Int32ul,
        'guid_high' / Int32ul,
    ),
)
