from typing import List, Tuple

from pony import orm

from database import world
from world_server import op_code, router, session
from world_server.packets import tutorial_flag


@router.Handler(op_code.Client.TUTORIAL_FLAG)
@orm.db_session
def handle_tutorial_flag(pkt: tutorial_flag.ClientTutorialFlag,
                         session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    player = world.Player[session.player_id]
    player.tutorials[pkt.flag] = True
    return []
