from typing import List, Tuple

from pony import orm

from database import world
from world_server import op_code, router, session
from world_server.packets import auto_equip_item, inventory_change_failure


def _error(code: inventory_change_failure.ErrorCode, **kwargs) -> List[Tuple[op_code.Server, bytes]]:
    return [(
        op_code.Server.INVENTORY_CHANGE_FAILURE,
        inventory_change_failure.ServerInventoryChangeFailure.build(dict(
            code=code,
            result=dict(**kwargs),
        )),
    )]


@router.Handler(op_code.Client.AUTO_EQUIP_ITEM)
@orm.db_session
def handler(pkt: auto_equip_item.ClientAutoEquipItem, session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    player = world.Player[session.player_id]

    # Find the item we want to equip.
    slot = player.get_item(pkt.container_slot, pkt.item_slot)
    if not slot.item:
        return []

    if isinstance(slot.item, world.Container):
        for _, bag in sorted(player.bags().items()):
            if not bag.item:
                bag.item = slot.item
                slot.item = None
                return []

        return _error(
            code=inventory_change_failure.ErrorCode.BAG_FULL,
            item1_guid=slot.item.guid,
            required_level=None,
        )

    return []
