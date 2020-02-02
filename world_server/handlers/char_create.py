import enum
from typing import List, Tuple

from pony import orm

from database.dbc import constants as c
from database.world.account import Account
from database.world.game_object.player import Player
from database.world.realm import Realm
from world_server import config, op_code, router, session
from world_server.packets import char_create


class ResponseCode(enum.IntEnum):
    ACCOUNT_LIMIT = 0x35
    DISABLED = 0x32  # "creation of characters is currently disabled"
    ERROR = 0x2F  # "error creating character"
    FAILED = 0x30  # "character creation failed"
    IN_PROGRESS = 0x2D  # "creating character"
    NAME_IN_USE = 0x31
    ONLY_EXISTING = 0x37  # "only players who already have characters on this realm are currently allowed to create characters"
    PVP_TEAMS_VIOLATION = 0x33  # "you cannot have both a Horde and an Alliance character on the same PvP realm"
    SERVER_LIMIT = 0x34
    SERVER_QUEUE = 0x36  # "This server is currently queued and new character creation is disabled"
    SUCCESS = 0x2E


@router.Handler(op_code.Client.CHAR_CREATE)
@orm.db_session
def handle_char_create(
        pkt: char_create.ClientCharCreate,
        session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    account = Account[session.account_name]
    realm = Realm[session.realm_name]

    # Account limit.
    if len(account.characters) >= config.MAX_CHARACTERS_PER_ACCOUNT:
        return [(
            op_code.Server.CHAR_CREATE,
            char_create.ServerCharCreate.build(
                dict(error=ResponseCode.ACCOUNT_LIMIT)),
        )]

    # Server limit.
    if orm.count(p for p in Player if p.account == account
                 and p.realm == realm) > config.MAX_CHARACTERS_PER_REALM:
        return [(
            op_code.Server.CHAR_CREATE,
            char_create.ServerCharCreate.build(
                dict(error=ResponseCode.SERVER_LIMIT)),
        )]

    # Name already in use.
    if orm.count(p for p in Player if p.name.upper() == pkt.name.upper()) > 0:
        return [(
            op_code.Server.CHAR_CREATE,
            char_create.ServerCharCreate.build(
                dict(error=ResponseCode.NAME_IN_USE)),
        )]

    Player.New(
        account=account,
        realm=realm,
        name=pkt.name,
        race=c.Race(pkt.race),
        class_=c.Class(pkt.class_),
        gender=c.Gender(pkt.gender),
        skin_color=pkt.skin_color,
        face=pkt.face,
        hair_style=pkt.hair_style,
        hair_color=pkt.hair_color,
        feature=pkt.feature,
    )

    return [(
        op_code.Server.CHAR_CREATE,
        char_create.ServerCharCreate.build(dict(error=ResponseCode.SUCCESS)),
    )]