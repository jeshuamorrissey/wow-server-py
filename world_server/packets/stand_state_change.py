from construct import Int32ul, Struct

from world_server import op_code, router

ClientStandStateChange = router.ClientPacket.Register(
    op_code.Client.STAND_STATE_CHANGE,
    Struct('state' / Int32ul),
)
