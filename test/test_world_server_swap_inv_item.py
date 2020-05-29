import sys

import pytest
from pony import orm

from database import enums, game, world
from world_server import op_code, system
from world_server.handlers import swap_inv_item as handler
from world_server.packets import inventory_change_failure
from world_server.packets import swap_inv_item as packet


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


def test_handle_swap_inv_item_src_out_of_range(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    client_pkt = packet.ClientSwapInvItem.parse(packet.ClientSwapInvItem.build(dict(
        src_slot=98,
        dst_slot=0,
    )))

    response_pkts = handler.handle_swap_inv_item(client_pkt, mock_session)
    assert len(response_pkts) == 0


def test_handle_swap_inv_item_dst_out_of_range(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    client_pkt = packet.ClientSwapInvItem.parse(packet.ClientSwapInvItem.build(dict(
        src_slot=0,
        dst_slot=98,
    )))

    response_pkts = handler.handle_swap_inv_item(client_pkt, mock_session)
    assert len(response_pkts) == 0


def test_handle_swap_inv_item_no_src_item(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    client_pkt = packet.ClientSwapInvItem.parse(packet.ClientSwapInvItem.build(dict(
        src_slot=0,
        dst_slot=1,
    )))

    response_pkts = handler.handle_swap_inv_item(client_pkt, mock_session)
    assert len(response_pkts) == 0


def test_handle_swap_inv_item_no_dst_valid_swap(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    mock_system = mocker.MagicMock()
    system.Register.SYSTEMS[system.System.ID.UPDATER] = mock_system

    item = world.Item.New(base_item=game.ItemTemplate[16795])
    fake_db.flush()
    player.equipment()[enums.EquipmentSlot.HEAD].item = item
    player.backpack()[0].item = None

    client_pkt = packet.ClientSwapInvItem.parse(
        packet.ClientSwapInvItem.build(
            dict(
                src_slot=enums.EquipmentSlot.HEAD,
                dst_slot=enums.InventorySlots.BACKPACK_START,
            )))

    assert player.equipment().get(enums.EquipmentSlot.HEAD).item == item
    assert player.backpack()[0].item is None

    update_fields = player.update_fields()
    assert update_fields[enums.PlayerFields.VISIBLE_ITEM_START + 2] == item.entry()

    response_pkts = handler.handle_swap_inv_item(client_pkt, mock_session)
    assert len(response_pkts) == 0

    mock_system.update_object.assert_has_calls([
        mocker.call(item),
        mocker.call(player),
    ], any_order=True)

    assert player.equipment().get(enums.EquipmentSlot.HEAD).item is None
    assert player.backpack()[0].item == item

    update_fields = player.update_fields()
    assert update_fields[enums.PlayerFields.VISIBLE_ITEM_START + 2] == 0


def test_handle_swap_inv_item_no_dst_invalid_swap(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    item = world.Item.New(base_item=game.ItemTemplate[16795])
    fake_db.flush()
    player.equipment()[enums.EquipmentSlot.HEAD].item = item
    player.backpack()[0].item = None

    client_pkt = packet.ClientSwapInvItem.parse(
        packet.ClientSwapInvItem.build(dict(
            src_slot=enums.EquipmentSlot.HEAD,
            dst_slot=enums.InventorySlots.BAG_START,
        )))

    assert player.equipment().get(enums.EquipmentSlot.HEAD).item == item
    assert player.backpack()[0].item is None

    response_pkts = handler.handle_swap_inv_item(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = inventory_change_failure.ServerInventoryChangeFailure.parse(response_bytes)
    assert response_op == op_code.Server.INVENTORY_CHANGE_FAILURE
    assert response_pkt.code == enums.InventoryChangeError.ITEM_DOESNT_GO_TO_SLOT

    assert player.equipment().get(enums.EquipmentSlot.HEAD).item == item
    assert player.backpack()[0].item is None


def test_handle_swap_inv_item_with_dst_valid_swap(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    mock_system = mocker.MagicMock()
    system.Register.SYSTEMS[system.System.ID.UPDATER] = mock_system

    item = world.Item.New(base_item=game.ItemTemplate[16795])
    item2 = world.Item.New(base_item=game.ItemTemplate[12752])
    fake_db.flush()
    player.equipment()[enums.EquipmentSlot.HEAD].item = item
    player.backpack()[0].item = item2

    client_pkt = packet.ClientSwapInvItem.parse(
        packet.ClientSwapInvItem.build(
            dict(
                src_slot=enums.EquipmentSlot.HEAD,
                dst_slot=enums.InventorySlots.BACKPACK_START,
            )))

    assert player.equipment().get(enums.EquipmentSlot.HEAD).item == item
    assert player.backpack()[0].item == item2

    response_pkts = handler.handle_swap_inv_item(client_pkt, mock_session)
    assert len(response_pkts) == 0

    mock_system.update_object.assert_has_calls(
        [mocker.call(item), mocker.call(item2), mocker.call(player)], any_order=True)

    assert player.equipment().get(enums.EquipmentSlot.HEAD).item == item2
    assert player.backpack()[0].item == item


def test_handle_swap_inv_item_with_dst_invalid_swap(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    item = world.Item.New(base_item=game.ItemTemplate[16795])
    item2 = world.Item.New(base_item=game.ItemTemplate[16800])
    fake_db.flush()
    player.equipment()[enums.EquipmentSlot.HEAD].item = item
    player.backpack()[0].item = item2

    client_pkt = packet.ClientSwapInvItem.parse(
        packet.ClientSwapInvItem.build(
            dict(
                src_slot=enums.EquipmentSlot.HEAD,
                dst_slot=enums.InventorySlots.BACKPACK_START,
            )))

    assert player.equipment().get(enums.EquipmentSlot.HEAD).item == item
    assert player.backpack()[0].item == item2

    response_pkts = handler.handle_swap_inv_item(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = inventory_change_failure.ServerInventoryChangeFailure.parse(response_bytes)
    assert response_op == op_code.Server.INVENTORY_CHANGE_FAILURE
    assert response_pkt.code == enums.InventoryChangeError.ITEM_DOESNT_GO_TO_SLOT

    assert player.equipment().get(enums.EquipmentSlot.HEAD).item == item
    assert player.backpack()[0].item == item2


def test_handle_swap_inv_item_with_container_with_item_inside_valid(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    bag = world.Container.New(base_item=game.ItemTemplate[14156])
    item = world.Item.New(base_item=game.ItemTemplate[16800])
    fake_db.flush()
    bag.items()[0].item = item
    player.bags()[0].item = bag
    player.bags()[1].item = None

    client_pkt = packet.ClientSwapInvItem.parse(
        packet.ClientSwapInvItem.build(
            dict(
                src_slot=enums.InventorySlots.BAG_START,
                dst_slot=enums.InventorySlots.BAG_START + 1,
            )))

    assert player.bags()[0].item == bag
    assert player.bags()[1].item is None
    assert bag.items()[0].item == item

    response_pkts = handler.handle_swap_inv_item(client_pkt, mock_session)

    assert len(response_pkts) == 0

    assert player.bags()[0].item is None
    assert player.bags()[1].item == bag
    assert bag.items()[0].item == item


def test_handle_swap_inv_item_with_container_with_item_inside_invalid(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    bag = world.Container.New(base_item=game.ItemTemplate[14156])
    item = world.Item.New(base_item=game.ItemTemplate[16800])
    fake_db.flush()
    bag.items()[0].item = item
    player.bags()[0].item = bag
    player.backpack()[0].item = None

    client_pkt = packet.ClientSwapInvItem.parse(
        packet.ClientSwapInvItem.build(
            dict(
                src_slot=enums.InventorySlots.BAG_START,
                dst_slot=enums.InventorySlots.BACKPACK_START,
            )))

    assert player.bags()[0].item == bag
    assert bag.items()[0].item == item
    assert player.backpack()[0].item == None

    response_pkts = handler.handle_swap_inv_item(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = inventory_change_failure.ServerInventoryChangeFailure.parse(response_bytes)
    assert response_op == op_code.Server.INVENTORY_CHANGE_FAILURE
    assert response_pkt.code == enums.InventoryChangeError.CAN_ONLY_DO_WITH_EMPTY_BAGS

    assert player.bags()[0].item == bag
    assert bag.items()[0].item == item
    assert player.backpack()[0].item == None


def test_handle_swap_inv_item_with_dst_container_with_item_inside_valid(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    bag = world.Container.New(base_item=game.ItemTemplate[14156])
    item = world.Item.New(base_item=game.ItemTemplate[16800])
    bag2 = world.Container.New(base_item=game.ItemTemplate[14156])
    item2 = world.Item.New(base_item=game.ItemTemplate[16800])
    fake_db.flush()
    bag.items()[0].item = item
    player.bags()[0].item = bag

    bag2.items()[0].item = item2
    player.bags()[1].item = bag2

    client_pkt = packet.ClientSwapInvItem.parse(
        packet.ClientSwapInvItem.build(
            dict(
                src_slot=enums.InventorySlots.BAG_START,
                dst_slot=enums.InventorySlots.BAG_START + 1,
            )))

    assert player.bags()[0].item == bag
    assert player.bags()[1].item == bag2
    assert bag.items()[0].item == item
    assert bag2.items()[0].item == item2

    response_pkts = handler.handle_swap_inv_item(client_pkt, mock_session)

    assert len(response_pkts) == 0

    assert player.bags()[0].item == bag2
    assert player.bags()[1].item == bag
    assert bag.items()[0].item == item
    assert bag2.items()[0].item == item2


def test_handle_swap_inv_item_with_dst_container_with_item_inside_invalid(mocker, fake_db):
    player = _create_player(fake_db)

    mock_session = mocker.MagicMock()
    mock_session.player_id = player.id

    bag = world.Container.New(base_item=game.ItemTemplate[14156])
    item = world.Item.New(base_item=game.ItemTemplate[16800])
    item2 = world.Item.New(base_item=game.ItemTemplate[16800])
    fake_db.flush()
    bag.items()[0].item = item
    player.bags()[0].item = bag
    player.backpack()[0].item = item2

    client_pkt = packet.ClientSwapInvItem.parse(
        packet.ClientSwapInvItem.build(
            dict(
                src_slot=enums.InventorySlots.BACKPACK_START,
                dst_slot=enums.InventorySlots.BAG_START,
            )))

    assert player.bags()[0].item == bag
    assert bag.items()[0].item == item
    assert player.backpack()[0].item == item2

    response_pkts = handler.handle_swap_inv_item(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = inventory_change_failure.ServerInventoryChangeFailure.parse(response_bytes)
    assert response_op == op_code.Server.INVENTORY_CHANGE_FAILURE
    assert response_pkt.code == enums.InventoryChangeError.ITEM_DOESNT_GO_TO_SLOT

    assert player.bags()[0].item == bag
    assert bag.items()[0].item == item
    assert player.backpack()[0].item == item2
