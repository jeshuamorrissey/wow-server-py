import sys

import pytest
from pony import orm

from database import enums, game, world
from world_server import op_code, system
from world_server.handlers import swap_item as handler
from world_server.packets import inventory_change_failure
from world_server.packets import swap_item as packet


def _create_player(fake_db) -> world.Player:
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

    return player


def test_handle_swap_item_bag_to_bag_with_dst(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    mock_system = mocker.MagicMock()
    system.Register.SYSTEMS[system.System.ID.UPDATER] = mock_system

    item = world.Item.New(base_item=game.ItemTemplate[16795])
    item2 = world.Item.New(base_item=game.ItemTemplate[16795])
    bag = world.Container.New(base_item=game.ItemTemplate[14156])
    bag2 = world.Container.New(base_item=game.ItemTemplate[14156])

    fake_db.flush()

    player.bags()[0].item = bag
    player.bags()[1].item = bag2
    bag.items()[0].item = item
    bag2.items()[0].item = item2

    client_pkt = packet.ClientSwapItem.parse(
        packet.ClientSwapItem.build(
            dict(
                source_bag=enums.InventorySlots.BAG_START,
                source_slot=0,
                dest_bag=enums.InventorySlots.BAG_START + 1,
                dest_slot=0,
            )))

    assert bag.items()[0].item == item
    assert bag2.items()[0].item == item2
    assert player.bags()[0].item == bag
    assert player.bags()[1].item == bag2

    assert bag.update_fields()[enums.ContainerFields.SLOT_1] == item.guid
    assert item.update_fields()[enums.ItemFields.CONTAINED] == bag.guid
    assert bag2.update_fields()[enums.ContainerFields.SLOT_1] == item2.guid
    assert item2.update_fields()[enums.ItemFields.CONTAINED] == bag2.guid

    response_pkts = handler.handle_swap_item(client_pkt, mock_session)
    assert len(response_pkts) == 0

    mock_system.update_object.assert_has_calls([
        mocker.call(bag),
        mocker.call(bag2),
        mocker.call(item),
        mocker.call(item2),
    ],
                                               any_order=True)

    assert bag.items()[0].item == item2
    assert bag2.items()[0].item == item
    assert player.bags()[0].item == bag
    assert player.bags()[1].item == bag2

    assert bag.update_fields()[enums.ContainerFields.SLOT_1] == item2.guid
    assert item.update_fields()[enums.ItemFields.CONTAINED] == bag2.guid
    assert bag2.update_fields()[enums.ContainerFields.SLOT_1] == item.guid
    assert item2.update_fields()[enums.ItemFields.CONTAINED] == bag.guid


def test_handle_swap_item_bag_to_bag_no_dst(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    mock_system = mocker.MagicMock()
    system.Register.SYSTEMS[system.System.ID.UPDATER] = mock_system

    item = world.Item.New(base_item=game.ItemTemplate[16795])
    bag = world.Container.New(base_item=game.ItemTemplate[14156])
    bag2 = world.Container.New(base_item=game.ItemTemplate[14156])

    fake_db.flush()

    player.bags()[0].item = bag
    player.bags()[1].item = bag2
    bag.items()[0].item = item
    bag2.items()[0].item = None

    client_pkt = packet.ClientSwapItem.parse(
        packet.ClientSwapItem.build(
            dict(
                source_bag=enums.InventorySlots.BAG_START,
                source_slot=0,
                dest_bag=enums.InventorySlots.BAG_START + 1,
                dest_slot=0,
            )))

    assert bag.items()[0].item == item
    assert bag2.items()[0].item == None
    assert player.bags()[0].item == bag
    assert player.bags()[1].item == bag2

    assert bag.update_fields()[enums.ContainerFields.SLOT_1] == item.guid
    assert item.update_fields()[enums.ItemFields.CONTAINED] == bag.guid
    assert bag2.update_fields()[enums.ContainerFields.SLOT_1] == 0

    response_pkts = handler.handle_swap_item(client_pkt, mock_session)
    assert len(response_pkts) == 0

    mock_system.update_object.assert_has_calls([
        mocker.call(bag),
        mocker.call(bag2),
        mocker.call(item),
    ],
                                               any_order=True)

    assert bag.items()[0].item == None
    assert bag2.items()[0].item == item
    assert player.bags()[0].item == bag
    assert player.bags()[1].item == bag2

    assert bag.update_fields()[enums.ContainerFields.SLOT_1] == 0
    assert item.update_fields()[enums.ItemFields.CONTAINED] == bag2.guid
    assert bag2.update_fields()[enums.ContainerFields.SLOT_1] == item.guid


def test_handle_swap_item_inv_to_bag_with_dst(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    mock_system = mocker.MagicMock()
    system.Register.SYSTEMS[system.System.ID.UPDATER] = mock_system

    item = world.Item.New(base_item=game.ItemTemplate[16795])
    item2 = world.Item.New(base_item=game.ItemTemplate[16795])
    bag = world.Container.New(base_item=game.ItemTemplate[14156])

    fake_db.flush()

    player.bags()[0].item = bag
    bag.items()[0].item = item
    player.backpack()[0].item = item2

    client_pkt = packet.ClientSwapItem.parse(
        packet.ClientSwapItem.build(
            dict(
                source_bag=255,
                source_slot=enums.InventorySlots.BACKPACK_START,
                dest_bag=enums.InventorySlots.BAG_START,
                dest_slot=0,
            )))

    assert player.bags()[0].item == bag
    assert bag.items()[0].item == item
    assert player.backpack()[0].item == item2

    assert bag.update_fields()[enums.ContainerFields.SLOT_1] == item.guid
    assert item.update_fields()[enums.ItemFields.CONTAINED] == bag.guid
    assert item2.update_fields()[enums.ItemFields.CONTAINED] == player.guid
    assert player.update_fields()[enums.PlayerFields.INVENTORY_START +
                                  (enums.InventorySlots.BACKPACK_START * 2)] == item2.guid

    response_pkts = handler.handle_swap_item(client_pkt, mock_session)
    assert len(response_pkts) == 0

    mock_system.update_object.assert_has_calls([
        mocker.call(bag),
        mocker.call(item),
        mocker.call(item2),
        mocker.call(player),
    ],
                                               any_order=True)

    assert player.bags()[0].item == bag
    assert bag.items()[0].item == item2
    assert player.backpack()[0].item == item

    assert bag.update_fields()[enums.ContainerFields.SLOT_1] == item2.guid
    assert item.update_fields()[enums.ItemFields.CONTAINED] == player.guid
    assert item2.update_fields()[enums.ItemFields.CONTAINED] == bag.guid
    assert player.update_fields()[enums.PlayerFields.INVENTORY_START +
                                  (enums.InventorySlots.BACKPACK_START * 2)] == item.guid


def test_handle_swap_item_inv_to_bag_no_dst(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    mock_system = mocker.MagicMock()
    system.Register.SYSTEMS[system.System.ID.UPDATER] = mock_system

    item2 = world.Item.New(base_item=game.ItemTemplate[16795])
    bag = world.Container.New(base_item=game.ItemTemplate[14156])

    fake_db.flush()

    player.bags()[0].item = bag
    bag.items()[0].item = None
    player.backpack()[0].item = item2

    client_pkt = packet.ClientSwapItem.parse(
        packet.ClientSwapItem.build(
            dict(
                source_bag=255,
                source_slot=enums.InventorySlots.BACKPACK_START,
                dest_bag=enums.InventorySlots.BAG_START,
                dest_slot=0,
            )))

    assert player.bags()[0].item == bag
    assert bag.items()[0].item == None
    assert player.backpack()[0].item == item2

    assert bag.update_fields()[enums.ContainerFields.SLOT_1] == 0
    assert item2.update_fields()[enums.ItemFields.CONTAINED] == player.guid
    assert player.update_fields()[enums.PlayerFields.INVENTORY_START +
                                  (enums.InventorySlots.BACKPACK_START * 2)] == item2.guid

    response_pkts = handler.handle_swap_item(client_pkt, mock_session)
    assert len(response_pkts) == 0

    mock_system.update_object.assert_has_calls([
        mocker.call(bag),
        mocker.call(item2),
        mocker.call(player),
    ],
                                               any_order=True)

    assert player.bags()[0].item == bag
    assert bag.items()[0].item == item2
    assert player.backpack()[0].item == None

    assert bag.update_fields()[enums.ContainerFields.SLOT_1] == item2.guid
    assert item2.update_fields()[enums.ItemFields.CONTAINED] == bag.guid
    assert player.update_fields()[enums.PlayerFields.INVENTORY_START + (enums.InventorySlots.BACKPACK_START * 2)] == 0


def test_handle_swap_item_bag_to_inv_with_dst(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    mock_system = mocker.MagicMock()
    system.Register.SYSTEMS[system.System.ID.UPDATER] = mock_system

    item = world.Item.New(base_item=game.ItemTemplate[16795])
    item2 = world.Item.New(base_item=game.ItemTemplate[16795])
    bag = world.Container.New(base_item=game.ItemTemplate[14156])

    fake_db.flush()

    player.bags()[0].item = bag
    bag.items()[0].item = item
    player.backpack()[0].item = item2

    client_pkt = packet.ClientSwapItem.parse(
        packet.ClientSwapItem.build(
            dict(
                source_bag=enums.InventorySlots.BAG_START,
                source_slot=0,
                dest_bag=255,
                dest_slot=enums.InventorySlots.BACKPACK_START,
            )))

    assert player.bags()[0].item == bag
    assert bag.items()[0].item == item
    assert player.backpack()[0].item == item2

    assert bag.update_fields()[enums.ContainerFields.SLOT_1] == item.guid
    assert item.update_fields()[enums.ItemFields.CONTAINED] == bag.guid
    assert item2.update_fields()[enums.ItemFields.CONTAINED] == player.guid
    assert player.update_fields()[enums.PlayerFields.INVENTORY_START +
                                  (enums.InventorySlots.BACKPACK_START * 2)] == item2.guid

    response_pkts = handler.handle_swap_item(client_pkt, mock_session)
    assert len(response_pkts) == 0

    mock_system.update_object.assert_has_calls([
        mocker.call(bag),
        mocker.call(item),
        mocker.call(item2),
        mocker.call(player),
    ],
                                               any_order=True)

    assert player.bags()[0].item == bag
    assert bag.items()[0].item == item2
    assert player.backpack()[0].item == item

    assert bag.update_fields()[enums.ContainerFields.SLOT_1] == item2.guid
    assert item.update_fields()[enums.ItemFields.CONTAINED] == player.guid
    assert item2.update_fields()[enums.ItemFields.CONTAINED] == bag.guid
    assert player.update_fields()[enums.PlayerFields.INVENTORY_START +
                                  (enums.InventorySlots.BACKPACK_START * 2)] == item.guid


def test_handle_swap_item_bag_to_inv_no_dst(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    mock_system = mocker.MagicMock()
    system.Register.SYSTEMS[system.System.ID.UPDATER] = mock_system

    item = world.Item.New(base_item=game.ItemTemplate[16795])
    bag = world.Container.New(base_item=game.ItemTemplate[14156])

    fake_db.flush()

    player.bags()[0].item = bag
    bag.items()[0].item = item
    player.backpack()[0].item = None

    client_pkt = packet.ClientSwapItem.parse(
        packet.ClientSwapItem.build(
            dict(
                source_bag=enums.InventorySlots.BAG_START,
                source_slot=0,
                dest_bag=255,
                dest_slot=enums.InventorySlots.BACKPACK_START,
            )))

    assert player.bags()[0].item == bag
    assert bag.items()[0].item == item
    assert player.backpack()[0].item == None

    assert bag.update_fields()[enums.ContainerFields.SLOT_1] == item.guid
    assert item.update_fields()[enums.ItemFields.CONTAINED] == bag.guid
    assert player.update_fields()[enums.PlayerFields.INVENTORY_START + (enums.InventorySlots.BACKPACK_START * 2)] == 0

    response_pkts = handler.handle_swap_item(client_pkt, mock_session)
    assert len(response_pkts) == 0

    mock_system.update_object.assert_has_calls([
        mocker.call(bag),
        mocker.call(item),
        mocker.call(player),
    ],
                                               any_order=True)

    assert player.bags()[0].item == bag
    assert bag.items()[0].item == None
    assert player.backpack()[0].item == item

    assert bag.update_fields()[enums.ContainerFields.SLOT_1] == 0
    assert item.update_fields()[enums.ItemFields.CONTAINED] == player.guid
    assert player.update_fields()[enums.PlayerFields.INVENTORY_START +
                                  (enums.InventorySlots.BACKPACK_START * 2)] == item.guid
