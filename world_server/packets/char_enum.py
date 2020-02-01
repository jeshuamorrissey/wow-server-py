from construct import Struct

from world_server import op_code, router

ClientCharEnum = router.ClientPacket.Register(
    op_code.Client.CHAR_ENUM,
    Struct(),
)
