import enum
import io
import logging
import sys
import unittest
from typing import Text
from unittest import mock


import pytest

from database import data, enums
from login_server import op_code
from login_server.handlers import realmlist as handler
from login_server.packets import realmlist as packet


def test_handle_realmlist(mocker, fake_db):
    # Setup database.
    account = fake_db.Account(name='account', salt_str='11', verifier_str='22')
    account2 = fake_db.Account(name='account2', salt_str='11', verifier_str='22')
    r1 = fake_db.Realm(name='r1', hostport='r1')
    r2 = fake_db.Realm(name='r2', hostport='r2')
    fake_db.Player.New(
        account,
        r1,
        'c1',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    fake_db.Player.New(
        account,
        r1,
        'c2',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    fake_db.Player.New(
        account,
        r2,
        'c3',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    fake_db.Player.New(
        account2,
        r1,
        'c4',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    client_pkt = packet.ClientRealmlist.parse(packet.ClientRealmlist.build(dict()))

    mock_session = mock.MagicMock()
    mock_session.account_name = 'account'
    mock_session.b = 1
    mock_session.B = 2

    response_pkts = handler.handle_realmlist(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerRealmlist.parse(response_bytes)
    assert response_op == op_code.Server.REALMLIST
    assert response_pkt.n_realms == 2
    assert response_pkt.realms[0].name == 'r1'
    assert response_pkt.realms[0].n_characters == 2
    assert response_pkt.realms[1].name == 'r2'
    assert response_pkt.realms[1].n_characters == 1


if __name__ == '__main__':
    sys.exit(pytest.main([__file__]))
