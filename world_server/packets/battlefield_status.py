from construct import Const, If, Int8ul, Int32ul, Struct, Switch

from database import enums
from world_server import op_code, router

ClientBattlefieldStatus = router.ClientPacket.Register(
    op_code.Client.BATTLEFIELD_STATUS,
    Struct(),
)

ServerBattlefieldStatus = Struct(
    'queue_slot' / Int32ul,
    'map_id' / Int32ul,
    'data' / If(
        lambda c: c.map_id != 0,
        Struct(
            Const(b'\x00'),
            'client_instance_id' / Int32ul,
            'status_id' / Int32ul,
            'times' / Switch(
                lambda c: c.status_id,
                {
                    enums.BattlegroundStatus.WAIT_QUEUE:
                    Struct(
                        'avg_wait_time_ms' / Int32ul,
                        'queue_time_ms' / Int32ul,
                    ),
                    enums.BattlegroundStatus.WAIT_JOIN:
                    Struct('remove_from_queue_ms' / Int32ul),
                    enums.BattlegroundStatus.IN_PROGRESS:
                    Struct(
                        'bg_auto_leave_ms' / Int32ul,
                        'since_bg_start_ms' / Int32ul,
                    ),
                },
                Const(b'\x00\x00\x00\x00'),
            ),
        )),
)
