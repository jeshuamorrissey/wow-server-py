from typing import List, Tuple

from pony import orm

from world_server import op_code, router, session
from world_server.packets import gm_get_ticket


@router.Handler(op_code.Client.GM_GET_TICKET)
@orm.db_session
def handler(pkt: gm_get_ticket.ClientGmGetTicket, session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    return [(
        op_code.Server.GM_GET_TICKET,
        gm_get_ticket.ServerGmGetTicket.build(dict(
            status=0xA0,
            ticket=None,
        )),
    )]
