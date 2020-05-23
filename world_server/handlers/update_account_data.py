from typing import List, Tuple

from pony import orm

from world_server import op_code, router, session
from world_server.packets import update_account_data


@router.Handler(op_code.Client.UPDATE_ACCOUNT_DATA)
@orm.db_session
def handle_ping(
        pkt: update_account_data.ClientUpdateAccountData,
        session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    # Non-implemented packet.
    # TODO(jeshua): What is this for? What are its fields?
    return []
