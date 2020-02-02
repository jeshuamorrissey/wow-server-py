from typing import List, Tuple

from pony import orm

from database.world.game_object.player import Player
from database.world.account import Account
from database.world.realm import Realm
from login_server import op_code, router, session
from login_server.packets import realmlist


@router.Handler(op_code.Client.REALMLIST)
@orm.db_session
def handle_realmlist(
        pkt: realmlist.ClientRealmlist,
        session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    account = Account[session.account_name]
    realms = [
        dict(
            icon=realm.type,
            flags=dict(
                is_full=False,  # TODO: calculate based on n chars
                is_recommended=realm.is_recommended,
                for_new_players=realm.for_new_players,
                is_offline=realm.is_offline,
                is_unavailable=realm.is_unavailable,
            ),
            name=realm.name,
            hostport=realm.hostport,
            population=0,  # TODO: calculate relative population
            n_characters=orm.count(
                p for p in Player
                if p.realm == realm and p.account == account),
        ) for realm in Realm.select()
    ]

    return [(
        op_code.Server.REALMLIST,
        realmlist.ServerRealmlist.build(dict(realms=realms)),
    )]
