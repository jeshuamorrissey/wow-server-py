from typing import List, Tuple

from pony import orm

from database import world
from world_server import op_code, router, session
from world_server.packets import set_action_button


@router.Handler(op_code.Client.SET_ACTION_BUTTON)
@orm.db_session
def handle_ping(pkt: set_action_button.ClientSetActionButton,
                session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    existing_button = world.PlayerActionButton.get(player=session.player_id, slot=pkt.slot)
    if existing_button:
        existing_button.action = pkt.action
        existing_button.type = pkt.type
    else:
        world.PlayerActionButton(
            slot=pkt.slot,
            action=pkt.action,
            type=pkt.type,
        )

    return []
