from typing import List, Tuple

from pony import orm

from common import srp
from database.world.account import Account
from world_server import op_code, router, session
from world_server.packets import char_enum


@router.Handler(op_code.Client.CHAR_ENUM)
@orm.db_session
def handle_char_enum(
        pkt: char_enum.ClientCharEnum,
        session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    account = Account[session.account_name]

    characters = []
    for character in account.characters:
        characters.append(
            dict(
                guid=character.id,
                name=character.name,
                race=character.race,
                class_=character.class_,
                gender=character.gender,
                appearance=dict(
                    skin=character.skin_color,
                    face=character.face,
                    hair_style=character.hair_style,
                    hair_color=character.hair_color,
                    feature=character.feature,
                ),
                level=character.level,
                location=dict(
                    zone=character.zone,
                    map=character.map,
                    x=character.x,
                    y=character.y,
                    z=character.z,
                ),
                guild_id=0,  # TODO
                flags=dict(is_ghost=character.is_ghost),
                first_login=0,  # TODO
                pet=dict(  # TODO
                    id=0,
                    level=0,
                    family=0,
                ),
                items=[dict(display_id=0, inventory_type=0)] * 19,  # TODO
                first_bag=dict(  # TODO
                    display_id=0,
                    inventory_type=0,
                ),
            ))

    return [(
        op_code.Server.CHAR_ENUM,
        char_enum.ServerCharEnum.build(dict(characters=characters)),
    )]
