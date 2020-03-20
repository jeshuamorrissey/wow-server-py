from construct import Struct

from world_server import op_code, router

ClientMeetingstoneInfo = router.ClientPacket.Register(
    op_code.Client.MEETINGSTONE_INFO,
    Struct(),
)
