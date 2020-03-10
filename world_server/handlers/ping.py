from typing import List, Tuple

from pony import orm

from world_server import op_code, router, session
from world_server.packets import ping, pong


@router.Handler(op_code.Client.PING)
@orm.db_session
def handle_ping(pkt: ping.ClientPing, session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    return [(
        op_code.Server.PONG,
        pong.ServerPong.build(dict(pong=pkt.ping)),
    )]
