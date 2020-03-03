from construct import Int32ul, Struct

from world_server import op_code, router

ClientQueryTime = router.ClientPacket.Register(
    op_code.Client.QUERY_TIME,
    Struct(),
)

ServerQueryTimeResponse = Struct('time' / Int32ul)
