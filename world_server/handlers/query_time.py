import time
from typing import List, Tuple

from pony import orm

from world_server import op_code, router, session
from world_server.packets import query_time


@router.Handler(op_code.Client.QUERY_TIME)
@orm.db_session
def handle_query_time(pkt: query_time.ClientQueryTime, session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    return [(
        op_code.Server.QUERY_TIME_RESPONSE,
        query_time.ServerQueryTimeResponse.build(dict(time=int(time.time()))),
    )]
