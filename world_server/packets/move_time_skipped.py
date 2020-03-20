from construct import Int32ul, Int64ul, Struct

from world_server import op_code, router

ClientMoveTimeSkipped = router.ClientPacket.Register(
    op_code.Client.MOVE_TIME_SKIPPED,
    Struct(
        'guid' / Int64ul,
        'time_skipped' / Int32ul,
    ),
)
