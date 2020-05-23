import enum
from typing import List, Tuple

from pony import orm

from common import srp
from database import world
from world_server import op_code, router, session
from world_server.packets import char_delete


class ResponseCode(enum.IntEnum):
    FAILED = 0x3A
    FAILED_LOCKED_FOR_TRANSFER = 0x3B
    IN_PROGRESS = 0x38
    SUCCESS = 0x39


@router.Handler(op_code.Client.CHAR_DELETE)
@orm.db_session
def handle_char_delete(
        pkt: char_delete.ClientCharDelete,
        session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    realm = world.Realm[session.realm_name]
    account = world.Account[session.account_name]

    to_delete = world.Player.get(realm=realm, account=account, id=pkt.guid_low)
    if not to_delete:
        session.log.error(
            f'Tried to delete character {pkt.guid_low}, but it does not exist')
        return [(
            op_code.Server.CHAR_DELETE,
            char_delete.ServerCharDelete.build(dict(error=ResponseCode.FAILED)),
        )]

    to_delete.delete()

    return [(
        op_code.Server.CHAR_DELETE,
        char_delete.ServerCharDelete.build(dict(error=ResponseCode.SUCCESS)),
    )]
