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
from world_server.handlers import char_enum as handler
from world_server.packets import auth_response
from world_server.packets import char_enum as packet


def test_handle_char_enum(mocker, fake_db):
    # Setup database.
    account = fake_db.Account(name='account',
                              salt_str='11',
                              verifier_str='22',
                              session_key_str='33')
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

    base_unit = fake_db.UnitTemplate.get(Name='Young Nightsaber')
    fake_db.Pet(
        base_unit=base_unit,
        name='Kiko',
        level=1,
        race=constants.ChrRaces[1],
        class_=constants.ChrClasses[base_unit.UnitClass],
        gender=enums.Gender.FEMALE,
        team=player.team,
        x=player.x + 2,
        y=player.y + 2,
        z=player.z,
        o=player.o,
        summoner=player,
        created_by=player,
        base_health=100,
        base_power=100,
    )

    fake_db.Player.New(
        id=50,
        account=account,
        realm=realm,
        name='test2',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.FEMALE,
    )

    client_pkt = packet.ClientCharEnum.parse(
        packet.ClientCharEnum.build(dict()))

    mock_session = mock.MagicMock()
    mock_session.account_name = 'account'
    mock_session.realm_name = 'r1'

    response_pkts = handler.handle_char_enum(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerCharEnum.parse(response_bytes)
    assert response_op == op_code.Server.CHAR_ENUM
    assert len(response_pkt.characters) == 2


if __name__ == '__main__':
    sys.exit(pytest.main([__file__]))
