from typing import List, Tuple

from pony import orm

from database import enums
from world_server import op_code, router, session
from world_server.packets import meetingstone_info, meetingstone_setqueue


@router.Handler(op_code.Client.MEETINGSTONE_INFO)
@orm.db_session
def handler(pkt: meetingstone_info.ClientMeetingstoneInfo,
            session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    # NOTE: Not implementing meeting stones; there will be other
    # ways to teleport to instances (if that is even something I want).
    return [(
        op_code.Server.MEETINGSTONE_SETQUEUE,
        meetingstone_setqueue.ServerMeetingstoneSetqueue.build(
            dict(
                area_id=0,
                status=enums.MeetingStoneQueueStatus.NONE,
            )),
    )]
