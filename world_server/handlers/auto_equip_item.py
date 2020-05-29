from typing import List, Tuple

from pony import orm

from database import enums, world
from world_server import op_code, router, session
from world_server.packets import auto_equip_item, inventory_change_failure


@router.Handler(op_code.Client.AUTO_EQUIP_ITEM)
@orm.db_session
def handler(pkt: auto_equip_item.ClientAutoEquipItem, session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    player = world.Player[session.player_id]
    ec = enums.InventoryChangeError

    # Find the item we want to equip.
    src_slot = player.get_item(pkt.container_slot, pkt.item_slot)
    dst_slot = None
    if not src_slot.item:
        return []

    if isinstance(src_slot.item, world.Container):
        for _, bag in sorted(player.bags().items()):
            if not bag.item:
                dst_slot = bag
                break

        if not dst_slot:
            return inventory_change_failure.error(
                code=ec.BAG_FULL,
                item1_guid=src_slot.item.guid,
                required_level=None,
            )

    else:
        # This is a normal item. So, we want to equip it.
        equipment_slots = src_slot.item.equipment_slot()
        if not equipment_slots:
            return inventory_change_failure.error(
                code=ec.NO_EQUIPMENT_SLOT_AVAILABLE,
                item1_guid=src_slot.item.guid,
                required_level=None,
            )

        # Find the appropriate slot, prefer empty ones if possible.
        dst_slot = player.equipment()[equipment_slots[0]]
        for equipment_slot in equipment_slots:
            slot = player.equipment()[equipment_slot]

            if not slot.item:
                dst_slot = slot

    # Make the swap.
    player.swap_items(src_slot, dst_slot)

    return []
