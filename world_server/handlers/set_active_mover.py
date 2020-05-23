from typing import List, Tuple

from pony import orm

from world_server import op_code, router, session
from world_server.packets import pong, set_active_mover


@router.Handler(op_code.Client.SET_ACTIVE_MOVER)
@orm.db_session
def handle_set_active_mover(
        pkt: set_active_mover.ClientSetActiveMover,
        session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    # TODO: implement this once you can move something else
    return []
