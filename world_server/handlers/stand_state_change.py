from typing import List, Tuple

from pony import orm

from database import world
from world_server import op_code, router, session
from world_server.packets import stand_state_change


@router.Handler(op_code.Client.STAND_STATE_CHANGE)
@orm.db_session
def handler(pkt: stand_state_change.ClientStandStateChange,
            session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    player = world.Player[session.player_id]
    player.stand_state = pkt.state
    return []
