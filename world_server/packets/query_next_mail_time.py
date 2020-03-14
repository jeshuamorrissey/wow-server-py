from construct import Float32l, Struct

from world_server import op_code, router

ClientQueryNextMailTime = router.ClientPacket.Register(
    op_code.Client.QUERY_NEXT_MAIL_TIME,
    Struct(),
)

ServerQueryNextMailTime = Struct('next_mail_time' / Float32l)
