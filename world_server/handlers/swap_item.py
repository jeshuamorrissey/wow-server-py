from typing import List, Tuple

from pony import orm

from database import enums, world
from world_server import op_code, router, session
from world_server.packets import inventory_change_failure, swap_item


@router.Handler(op_code.Client.SWAP_ITEM)
@orm.db_session
def handler(pkt: swap_item.ClientSwapItem,
            session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    player = world.Player[session.player_id]

    src_slot = player.get_item(pkt.source_bag, pkt.source_slot)
    dst_slot = player.get_item(pkt.dest_bag, pkt.dest_slot)

    if not src_slot.item:
        return inventory_change_failure.error(
            enums.InventoryChangeError.ITEM_NOT_FOUND)

    ## Validation
    # If neither slot can contain the other, then don't do anything.
    if not src_slot.can_contain(dst_slot.item) or not dst_slot.can_contain(
            src_slot.item):
        return inventory_change_failure.error(
            code=enums.InventoryChangeError.ITEM_DOESNT_GO_TO_SLOT)

    ## Do the swap.
    src_slot.item, dst_slot.item = dst_slot.item, src_slot.item

    return []
