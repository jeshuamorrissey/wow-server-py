from typing import List, Tuple

from pony import orm

from world_server import op_code, router, session
from world_server.packets import request_pet_info


@router.Handler(op_code.Client.REQUEST_PET_INFO)
@orm.db_session
def handler(pkt: request_pet_info.ClientRequestPetInfo,
            session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    return []
