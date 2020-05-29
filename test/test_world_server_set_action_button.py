import sys

import pytest

from database import enums, world
from world_server import op_code
from world_server.handlers import set_action_button as handler
from world_server.packets import set_action_button as packet


def test_handle_set_action_button_make_new(mocker, fake_db):
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

    client_pkt = packet.ClientSetActionButton.parse(packet.ClientSetActionButton.build(dict(
        slot=1,
        action=2,
        type=3,
    )))

    assert fake_db.PlayerActionButton.get(player=player, slot=1) is None

    response_pkts = handler.handle_set_action_button(client_pkt, mock_session)
    assert len(response_pkts) == 0

    action_button = fake_db.PlayerActionButton.get(player=player, slot=1)
    assert action_button is not None
    assert action_button.slot == 1
    assert action_button.action == 2
    assert action_button.type == 3


def test_handle_set_action_button_update_existing(mocker, fake_db):
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

    fake_db.PlayerActionButton(player=player, slot=1, action=2, type=3)

    client_pkt = packet.ClientSetActionButton.parse(packet.ClientSetActionButton.build(dict(
        slot=1,
        action=5,
        type=6,
    )))

    action_button = fake_db.PlayerActionButton.get(player=player, slot=1)
    assert action_button is not None
    assert action_button.slot == 1
    assert action_button.action == 2
    assert action_button.type == 3

    response_pkts = handler.handle_set_action_button(client_pkt, mock_session)
    assert len(response_pkts) == 0

    action_button = fake_db.PlayerActionButton.get(player=player, slot=1)
    assert action_button is not None
    assert action_button.slot == 1
    assert action_button.action == 5
    assert action_button.type == 6
