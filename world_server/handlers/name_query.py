from typing import List, Tuple

from pony import orm

from world_server import op_code, router, session
from world_server.packets import name_query
from database.world.game_object.player import Player


@router.Handler(op_code.Client.NAME_QUERY)
@orm.db_session
def handle_name_query(
        pkt: name_query.ClientNameQuery,
        session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    player = Player[pkt.guid]

    return [(
        op_code.Server.NAME_QUERY_RESPONSE,
        name_query.ServerNameQuery.build(
            dict(
                guid=player.guid,
                name=player.name,
                realm_name=player.realm.name,
                race=player.race,
                gender=player.gender,
                class_=player.class_,
            )),
    )]
