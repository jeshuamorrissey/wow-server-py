from construct import Int8ul, Int24ul, Struct

from world_server import op_code, router

ClientSetActionButton = router.ClientPacket.Register(
    op_code.Client.SET_ACTION_BUTTON,
    Struct(
        'slot' / Int8ul,
        'action' / Int24ul,
        'type' / Int8ul,
    ),
)
