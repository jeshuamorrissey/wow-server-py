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
from world_server.handlers import char_create as handler
from world_server.packets import auth_response
from world_server.packets import char_create as packet


def test_handle_char_create(mocker, fake_db):
    # Setup database.
    fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')
    fake_db.Realm(name='r1', hostport='r1')

    client_pkt = packet.ClientCharCreate.parse(
        packet.ClientCharCreate.build(
            dict(
                name='test',
                race=enums.EChrRaces.HUMAN,
                class_=enums.EChrClasses.WARRIOR,
                gender=enums.Gender.MALE,
                skin_color=1,
                face=2,
                hair_style=3,
                hair_color=4,
                feature=5,
                outfit_id=6,
            )))

    mock_session = mock.MagicMock()
    mock_session.account_name = 'account'
    mock_session.realm_name = 'r1'

    response_pkts = handler.handle_char_create(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerCharCreate.parse(response_bytes)
    assert response_op == op_code.Server.CHAR_CREATE
    assert response_pkt.error == handler.ResponseCode.SUCCESS

    player = fake_db.Player.get(name='test')
    assert player is not None
    assert player.race.id == enums.EChrRaces.HUMAN
    assert player.class_.id == enums.EChrClasses.WARRIOR


def test_handle_char_create_account_limit(mocker, fake_db):
    # Setup database.
    account = fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')
    realm = fake_db.Realm(name='r1', hostport='r1')
    realm2 = fake_db.Realm(name='r2', hostport='r1')
    fake_db.Player.New(
        id=10,
        account=account,
        realm=realm2,
        name='c4',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    client_pkt = packet.ClientCharCreate.parse(
        packet.ClientCharCreate.build(
            dict(
                name='test',
                race=enums.EChrRaces.HUMAN,
                class_=enums.EChrClasses.WARRIOR,
                gender=enums.Gender.MALE,
                skin_color=1,
                face=2,
                hair_style=3,
                hair_color=4,
                feature=5,
                outfit_id=6,
            )))

    mock_session = mock.MagicMock()
    mock_session.account_name = 'account'
    mock_session.realm_name = 'r1'

    mock_config = mocker.patch.object(handler, 'config')
    mock_config.MAX_CHARACTERS_PER_ACCOUNT = 1

    response_pkts = handler.handle_char_create(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerCharCreate.parse(response_bytes)
    assert response_op == op_code.Server.CHAR_CREATE
    assert response_pkt.error == handler.ResponseCode.ACCOUNT_LIMIT


def test_handle_char_create_server_limit(mocker, fake_db):
    # Setup database.
    account = fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')
    realm = fake_db.Realm(name='r1', hostport='r1')
    fake_db.Player.New(
        id=10,
        account=account,
        realm=realm,
        name='c4',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    client_pkt = packet.ClientCharCreate.parse(
        packet.ClientCharCreate.build(
            dict(
                name='test',
                race=enums.EChrRaces.HUMAN,
                class_=enums.EChrClasses.WARRIOR,
                gender=enums.Gender.MALE,
                skin_color=1,
                face=2,
                hair_style=3,
                hair_color=4,
                feature=5,
                outfit_id=6,
            )))

    mock_session = mock.MagicMock()
    mock_session.account_name = account.name
    mock_session.realm_name = realm.name

    mock_config = mocker.patch.object(handler, 'config')
    mock_config.MAX_CHARACTERS_PER_ACCOUNT = 100
    mock_config.MAX_CHARACTERS_PER_REALM = 1

    response_pkts = handler.handle_char_create(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerCharCreate.parse(response_bytes)
    assert response_op == op_code.Server.CHAR_CREATE
    assert handler.ResponseCode(response_pkt.error) == handler.ResponseCode.SERVER_LIMIT


def test_handle_char_create_name_in_use(mocker, fake_db):
    # Setup database.
    fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')
    account2 = fake_db.Account(name='account2', salt_str='11', verifier_str='22', session_key_str='33')
    realm = fake_db.Realm(name='r1', hostport='r1')
    fake_db.Player.New(
        id=10,
        account=account2,
        realm=realm,
        name='test',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    client_pkt = packet.ClientCharCreate.parse(
        packet.ClientCharCreate.build(
            dict(
                name='test',
                race=enums.EChrRaces.HUMAN,
                class_=enums.EChrClasses.WARRIOR,
                gender=enums.Gender.MALE,
                skin_color=1,
                face=2,
                hair_style=3,
                hair_color=4,
                feature=5,
                outfit_id=6,
            )))

    mock_session = mock.MagicMock()
    mock_session.account_name = 'account'
    mock_session.realm_name = 'r1'

    response_pkts = handler.handle_char_create(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerCharCreate.parse(response_bytes)
    assert response_op == op_code.Server.CHAR_CREATE
    assert response_pkt.error == handler.ResponseCode.NAME_IN_USE
