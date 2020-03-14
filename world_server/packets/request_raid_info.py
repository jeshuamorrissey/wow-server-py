from construct import Int32ul, Struct

from world_server import op_code, router

ClientRequestRaidInfo = router.ClientPacket.Register(
    op_code.Client.REQUEST_RAID_INFO,
    Struct(),
)
