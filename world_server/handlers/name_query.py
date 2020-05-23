from typing import List, Tuple

from pony import orm

from database import world
from world_server import op_code, router, session
from world_server.packets import name_query


@router.Handler(op_code.Client.NAME_QUERY)
@orm.db_session
def handle_name_query(
        pkt: name_query.ClientNameQuery,
        session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    player = world.Player[pkt.guid]

    return [(
        op_code.Server.NAME_QUERY_RESPONSE,
        name_query.ServerNameQuery.build(
            dict(
                guid=player.guid,
                name=player.name,
                realm_name=player.realm.name,
                race=player.race.id,
                gender=player.gender,
                class_=player.class_.id,
            )),
    )]
