import sys

import pytest

from database import enums, world
from world_server import op_code
from world_server.handlers import query_next_mail_time as handler
from world_server.packets import query_next_mail_time as packet


def test_handle_query_next_mail_time_no_mail(mocker, fake_db):
    mock_session = mocker.MagicMock()
    mock_session.player_id = 10

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

    client_pkt = packet.ClientQueryNextMailTime.parse(packet.ClientQueryNextMailTime.build(dict(guid=10)))

    response_pkts = handler.handle_query_next_mail_time(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerQueryNextMailTime.parse(response_bytes)
    assert response_op == op_code.Server.QUERY_NEXT_MAIL_TIME
    assert response_pkt.next_mail_time == -1


def test_handle_query_next_mail_time_with_mail(mocker, fake_db):
    mock_session = mocker.MagicMock()
    mock_session.player_id = 10

    account = fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')
    realm = fake_db.Realm(name='r1', hostport='r1')
    player = fake_db.Player.New(
        id=10,
        account=account,
        realm=realm,
        name='test',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    fake_db.PlayerMail(from_player=player, to_player=player, content='test')

    client_pkt = packet.ClientQueryNextMailTime.parse(packet.ClientQueryNextMailTime.build(dict(guid=10)))

    response_pkts = handler.handle_query_next_mail_time(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerQueryNextMailTime.parse(response_bytes)
    assert response_op == op_code.Server.QUERY_NEXT_MAIL_TIME
    assert response_pkt.next_mail_time == 0
