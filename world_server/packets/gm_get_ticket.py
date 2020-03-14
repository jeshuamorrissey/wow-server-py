from construct import Const, CString, Float32l, If, Int8ul, Int32ul, Struct

from world_server import op_code, router

ClientGmGetTicket = router.ClientPacket.Register(
    op_code.Client.GM_GET_TICKET,
    Struct(),
)

ServerGmGetTicket = Struct(
    'status' / Int32ul,
    'ticket' / If(
        lambda c: c.status == 0x06,
        Struct(
            'text' / CString('ascii'),
            'category' / Int8ul,
            'in_queue' / Float32l,
            'high_volume_threshold' / Float32l,
            'wait_time_estimate' / Float32l,
            Const(b'\x00'),
            Const(b'\x00'),
        ),
    ),
)
