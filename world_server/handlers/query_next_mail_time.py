from typing import List, Tuple

from pony import orm

from database import world
from world_server import op_code, router, session
from world_server.packets import query_next_mail_time


@router.Handler(op_code.Client.QUERY_NEXT_MAIL_TIME)
@orm.db_session
def handle_query_next_mail_time(pkt: query_next_mail_time.ClientQueryNextMailTime,
                                session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    player = world.Player[session.player_id]

    next_mail_time = -1
    if len(player.received_mail) > 0:
        next_mail_time = 0

    return [(
        op_code.Server.QUERY_NEXT_MAIL_TIME,
        query_next_mail_time.ServerQueryNextMailTime.build(dict(next_mail_time=next_mail_time)),
    )]
