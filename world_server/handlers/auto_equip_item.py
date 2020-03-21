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
    item = player.get_item(pkt.container_slot, pkt.item_slot)
    if not item:
        return []

    ## Now, figure out how to equip the item.
    # For containers, find the next free slot.
    if isinstance(item, world.Container):
        # TODO: if the bank pane is open, add it to a bank slot instead.
        used_slots = {eb.slot for eb in world.EquippedBag.select() if eb.owner == player}
        for slot in range(4):
            if slot not in used_slots:
                item.remove_from_slot()
                world.EquippedBag(owner=player, slot=slot, container=item)
                return []

        # Error: cannot equip.
        return _error(
            code=inventory_change_failure.ErrorCode.ITEM_CANT_BE_EQUIPPED,
            item1_guid=item.guid,
        )

    return []
