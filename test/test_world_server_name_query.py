import sys

import pytest

from database import world, enums
from world_server import op_code
from world_server.handlers import name_query as handler
from world_server.packets import name_query as packet


def test_handle_name_query(mocker, fake_db):
    mock_session = mocker.MagicMock()

    account = fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')
    realm = fake_db.Realm(name='r1', hostport='r1')
    fake_db.Player.New(
        id=10,
        account=account,
        realm=realm,
        name='test',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    client_pkt = packet.ClientNameQuery.parse(packet.ClientNameQuery.build(dict(guid=10)))

    response_pkts = handler.handle_name_query(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerNameQuery.parse(response_bytes)
    assert response_op == op_code.Server.NAME_QUERY_RESPONSE
    assert response_pkt.name == 'test'
    assert response_pkt.realm_name == 'r1'
