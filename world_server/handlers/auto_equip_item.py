from typing import List, Tuple

from pony import orm

from database import world
from world_server import op_code, router, session
from world_server.packets import auto_equip_item


@router.Handler(op_code.Client.AUTO_EQUIP_ITEM)
@orm.db_session
def handler(pkt: auto_equip_item.ClientAutoEquipItem, session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    player = world.Player[session.player_id]

    # Find the item we want to equip.
    item = player.get_item(pkt.container_slot, pkt.item_slot)
    if not item:
        return []

    # Now, figure out how to equip the item.
    if isinstance(item, world.Container):
        print('Equip container!')

    return []
