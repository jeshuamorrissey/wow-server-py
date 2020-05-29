import sys

import pytest
from pony import orm

from database import enums, world
from world_server import op_code, system
from world_server.handlers import stand_state_change as handler
from world_server.packets import stand_state_change as packet


def test_handle_stand_state_change(mocker, fake_db):
    mock_session = mocker.MagicMock()
    mock_session.player_id = 10

    mock_system = mocker.MagicMock()
    system.Register.SYSTEMS[system.System.ID.UPDATER] = mock_system

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
        stand_state=enums.StandState.STAND,
    )

    client_pkt = packet.ClientStandStateChange.parse(
        packet.ClientStandStateChange.build(dict(state=enums.StandState.KNEEL)))

    assert fake_db.Player.get(id=player.id).stand_state == enums.StandState.STAND
    assert fake_db.Player.get(id=player.id).update_fields()[enums.UnitFields.BYTES_1] & 0x00FF == enums.StandState.STAND

    response_pkts = handler.handle_stand_state_change(client_pkt, mock_session)
    assert len(response_pkts) == 0

    assert fake_db.Player.get(id=player.id).stand_state == enums.StandState.KNEEL

    orm.flush()
    mock_system.update_object.assert_called_once_with(player)
    assert fake_db.Player.get(id=player.id).update_fields()[enums.UnitFields.BYTES_1] & 0x00FF == enums.StandState.KNEEL
