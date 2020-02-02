from construct import Int32ul, Struct

from world_server import op_code, router

ClientPing = router.ClientPacket.Register(
    op_code.Client.PING,
    Struct(
        'ping' / Int32ul,
        'latency' / Int32ul,
    ),
)
