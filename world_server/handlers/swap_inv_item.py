from typing import List, Tuple

from pony import orm

from world_server import op_code, router, session
from world_server.packets import swap_inv_item


@router.Handler(op_code.Client.SWAP_INV_ITEM)
@orm.db_session
def handler(pkt: swap_inv_item.ClientSwapInvItem,
            session: session.Session) -> List[Tuple[op_code.Server, bytes]]:

    return []
