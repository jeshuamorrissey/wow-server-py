from typing import List, Tuple

from pony import orm

from common import srp
from database.account import Account
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
                location=dict(  # TODO
                    zone=0,
                    map=0,
                    x=0,
                    y=0,
                    z=0,
                ),
                guild_id=0,  # TODO
                flags=dict(
                    f0=False,
                    f1=False,
                    f2=False,
                    f3=False,
                    f4=False,
                    f5=False,
                    f6=False,
                    f7=False,
                    f8=False,
                    f9=False,
                    f10=False,
                    f11=False,
                    f12=False,
                    f13=False,
                    f14=False,
                    f15=False,
                    f16=False,
                    f17=False,
                    f18=False,
                    f19=False,
                    f20=False,
                    f21=False,
                    f22=False,
                    f23=False,
                    f24=False,
                    f25=False,
                    f26=False,
                    f27=False,
                    f28=False,
                    f29=False,
                    f30=False,
                    f31=False,
                ),
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
