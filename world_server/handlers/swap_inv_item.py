from typing import List, Tuple

from pony import orm

from database import enums, world
from world_server import op_code, router, session
from world_server.packets import inventory_change_failure, swap_inv_item

# SWAP_INV_ITEM is used to swap the position of two items in the _inventory_. This includes
# any item slot which is not part of another bag and is on the player (equipment, backpack,
# keyring, ...).


@router.Handler(op_code.Client.SWAP_INV_ITEM)
@orm.db_session
def handle_swap_inv_item(pkt: swap_inv_item.ClientSwapInvItem,
                         session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    player = world.Player[session.player_id]

    if (pkt.src_slot < 0 or pkt.src_slot > enums.InventorySlots.KEYRING_END or pkt.dst_slot < 0 or
            pkt.dst_slot > enums.InventorySlots.KEYRING_END):
        return []

    src_slot = world.PlayerInventorySlot.get(player=player, slot=pkt.src_slot)
    dst_slot = world.PlayerInventorySlot.get(player=player, slot=pkt.dst_slot)

    code = player.swap_items(src_slot, dst_slot)
    if code is not None and code != enums.InventoryChangeError.OK:
        return [(
            op_code.Server.INVENTORY_CHANGE_FAILURE,
            inventory_change_failure.ServerInventoryChangeFailure.build(
                dict(
                    code=code,
                    result=dict(
                        required_level=src_slot.item.base_item.RequiredLevel if src_slot.item else 0,
                        item1_guid=src_slot.item.guid if src_slot.item else 0,
                        item2_guid=dst_slot.item.guid if dst_slot.item else 0,
                    ),
                )),
        )]
    return []
