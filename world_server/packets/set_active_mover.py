from construct import Int64ul, Struct

from world_server import op_code, router

ClientSetActiveMover = router.ClientPacket.Register(
    op_code.Client.SET_ACTIVE_MOVER,
    Struct('guid' / Int64ul),
)
