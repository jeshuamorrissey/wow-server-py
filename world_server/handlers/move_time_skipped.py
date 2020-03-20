from typing import List, Tuple

from pony import orm

from world_server import op_code, router, session
from world_server.packets import move_time_skipped


@router.Handler(op_code.Client.MOVE_TIME_SKIPPED)
@orm.db_session
def handler(pkt: move_time_skipped.ClientMoveTimeSkipped,
            session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    return []
