import enum
import io
import logging
import sys
import unittest
from typing import Text
from unittest import mock


import pytest
from pony import orm

from database import constants, data, enums
from world_server import op_code, systems
from world_server.handlers import char_delete as handler
from world_server.packets import auth_response
from world_server.packets import char_delete as packet


def test_handle_char_delete(mocker, fake_db):
    # Setup database.
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

    client_pkt = packet.ClientCharDelete.parse(packet.ClientCharDelete.build(dict(
        guid_low=player.id,
        guid_high=0,
    )))

    mock_session = mock.MagicMock()
    mock_session.account_name = 'account'
    mock_session.realm_name = 'r1'

    response_pkts = handler.handle_char_delete(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerCharDelete.parse(response_bytes)
    assert response_op == op_code.Server.CHAR_DELETE
    assert response_pkt.error == handler.ResponseCode.SUCCESS

    player = fake_db.Player.get(name='test')
    assert player is None


def test_handle_char_delete_not_exists(mocker, fake_db):
    # Setup database.
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

    client_pkt = packet.ClientCharDelete.parse(packet.ClientCharDelete.build(dict(
        guid_low=player.id + 1,
        guid_high=0,
    )))

    mock_session = mock.MagicMock()
    mock_session.account_name = account.name
    mock_session.realm_name = realm.name

    response_pkts = handler.handle_char_delete(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerCharDelete.parse(response_bytes)
    assert response_op == op_code.Server.CHAR_DELETE
    assert response_pkt.error == handler.ResponseCode.FAILED


if __name__ == '__main__':
    sys.exit(pytest.main([__file__]))
