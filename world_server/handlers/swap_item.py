from typing import List, Tuple

from pony import orm

from database import enums, world
from world_server import op_code, router, session
from world_server.packets import inventory_change_failure, swap_item


@router.Handler(op_code.Client.SWAP_ITEM)
@orm.db_session
def handle_swap_item(pkt: swap_item.ClientSwapItem, session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    player = world.Player[session.player_id]

    src_slot = player.get_item(pkt.source_bag, pkt.source_slot)
    dst_slot = player.get_item(pkt.dest_bag, pkt.dest_slot)

    player.swap_items(src_slot, dst_slot)
    return []
