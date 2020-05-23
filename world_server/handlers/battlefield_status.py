from typing import List, Tuple

from pony import orm

from world_server import op_code, router, session
from world_server.packets import battlefield_status


@router.Handler(op_code.Client.BATTLEFIELD_STATUS)
@orm.db_session
def handler(pkt: battlefield_status.ClientBattlefieldStatus,
            session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    return [
        (
            op_code.Server.BATTLEFIELD_STATUS,
            battlefield_status.ServerBattlefieldStatus.build(
                dict(
                    queue_slot=0,
                    map_id=0,
                    data=None,
                )),
        ),
        (
            op_code.Server.BATTLEFIELD_STATUS,
            battlefield_status.ServerBattlefieldStatus.build(
                dict(
                    queue_slot=1,
                    map_id=0,
                    data=None,
                )),
        ),
        (
            op_code.Server.BATTLEFIELD_STATUS,
            battlefield_status.ServerBattlefieldStatus.build(
                dict(
                    queue_slot=2,
                    map_id=0,
                    data=None,
                )),
        ),
    ]
