import enum
import io
import logging
import sys
import unittest
from typing import Text
from unittest import mock

import pytest
from pony import orm

from database import data, enums
from world_server import op_code, systems
from world_server.handlers import auto_equip_item as handler
from world_server.packets import auth_response
from world_server.packets import auto_equip_item as packet
from world_server.packets import inventory_change_failure


def test_handle_auto_equip_item_weapon_in_slot(mocker, fake_db):
    # Setup database.
    account = fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')
    realm = fake_db.Realm(name='r1', hostport='r1')
    player = fake_db.Player.New(
        id=10,
        account=account,
        realm=realm,
        name='c4',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    player.backpack()[15].item = fake_db.Item.New(base_item=fake_db.ItemTemplate.get(name='Blackguard'))

    dst_item = player.equipment()[enums.EquipmentSlot.MAIN_HAND].item
    src_item = player.backpack()[15].item

    client_pkt = packet.ClientAutoEquipItem.parse(
        packet.ClientAutoEquipItem.build(dict(
            container_slot=255,
            item_slot=enums.InventorySlots.BACKPACK_START + 15,
        )))

    mock_session = mock.MagicMock()
    mock_session.player_id = player.id

    handler.handler(client_pkt, mock_session)

    # Make sure the database changed.
    assert player.backpack()[15].item == dst_item
    assert player.equipment()[enums.EquipmentSlot.MAIN_HAND].item == src_item


def test_handle_auto_equip_item_empty_slot(mocker, fake_db):
    # Setup database.
    account = fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')
    realm = fake_db.Realm(name='r1', hostport='r1')
    player = fake_db.Player.New(
        id=10,
        account=account,
        realm=realm,
        name='c4',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    player.backpack()[15].item = fake_db.Item.New(base_item=fake_db.ItemTemplate.get(name='Blackguard'))
    player.equipment()[enums.EquipmentSlot.MAIN_HAND].item = None

    src_item = player.backpack()[15].item

    client_pkt = packet.ClientAutoEquipItem.parse(
        packet.ClientAutoEquipItem.build(dict(
            container_slot=255,
            item_slot=enums.InventorySlots.BACKPACK_START + 15,
        )))

    mock_session = mock.MagicMock()
    mock_session.player_id = player.id

    handler.handler(client_pkt, mock_session)

    # Make sure the database changed.
    assert player.backpack()[15].item == None
    assert player.equipment()[enums.EquipmentSlot.MAIN_HAND].item == src_item


def test_handle_auto_equip_item_no_item_in_slot(mocker, fake_db):
    # Setup database.
    account = fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')
    realm = fake_db.Realm(name='r1', hostport='r1')
    player = fake_db.Player.New(
        id=10,
        account=account,
        realm=realm,
        name='c4',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    player.equipment()[enums.EquipmentSlot.MAIN_HAND].item = None

    dst_item = player.equipment()[enums.EquipmentSlot.MAIN_HAND].item

    client_pkt = packet.ClientAutoEquipItem.parse(
        packet.ClientAutoEquipItem.build(dict(
            container_slot=255,
            item_slot=enums.InventorySlots.BACKPACK_START + 15,
        )))

    mock_session = mock.MagicMock()
    mock_session.player_id = player.id

    handler.handler(client_pkt, mock_session)

    # Make sure the database changed.
    assert player.equipment()[enums.EquipmentSlot.MAIN_HAND].item == dst_item


def test_handle_auto_equip_item_container(mocker, fake_db):
    # Setup database.
    account = fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')
    realm = fake_db.Realm(name='r1', hostport='r1')
    player = fake_db.Player.New(
        id=10,
        account=account,
        realm=realm,
        name='c4',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    to_equip = fake_db.Container.New(base_item=fake_db.ItemTemplate.get(name='Mooncloth Bag'))
    player.backpack()[15].item = to_equip

    client_pkt = packet.ClientAutoEquipItem.parse(
        packet.ClientAutoEquipItem.build(dict(
            container_slot=255,
            item_slot=enums.InventorySlots.BACKPACK_START + 15,
        )))

    mock_session = mock.MagicMock()
    mock_session.player_id = player.id

    handler.handler(client_pkt, mock_session)

    # Make sure the database changed.
    assert player.bags()[0].item == to_equip


def test_handle_auto_equip_from_container(mocker, fake_db):
    # Setup database.
    account = fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')
    realm = fake_db.Realm(name='r1', hostport='r1')
    player = fake_db.Player.New(
        id=10,
        account=account,
        realm=realm,
        name='c4',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    player.bags()[0].item = fake_db.Container.New(base_item=fake_db.ItemTemplate.get(name='Mooncloth Bag'))
    player.bags()[0].item.items()[0].item = fake_db.Item.New(base_item=fake_db.ItemTemplate.get(name='Blackguard'))

    dst_item = player.equipment()[enums.EquipmentSlot.MAIN_HAND].item
    src_item = player.bags()[0].item.items()[0].item

    client_pkt = packet.ClientAutoEquipItem.parse(
        packet.ClientAutoEquipItem.build(dict(
            container_slot=enums.InventorySlots.BAG_START,
            item_slot=0,
        )))

    mock_session = mock.MagicMock()
    mock_session.player_id = player.id

    handler.handler(client_pkt, mock_session)

    # Make sure the database changed.
    assert player.bags()[0].item.items()[0].item == dst_item
    assert player.equipment()[enums.EquipmentSlot.MAIN_HAND].item == src_item


def test_handle_auto_equip_container_no_slots_left(mocker, fake_db):
    # Setup database.
    account = fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')
    realm = fake_db.Realm(name='r1', hostport='r1')
    player = fake_db.Player.New(
        id=10,
        account=account,
        realm=realm,
        name='c4',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    player.backpack()[15].item = fake_db.Container.New(base_item=fake_db.ItemTemplate.get(name='Mooncloth Bag'))
    player.bags()[0].item = fake_db.Container.New(base_item=fake_db.ItemTemplate.get(name='Mooncloth Bag'))
    player.bags()[1].item = fake_db.Container.New(base_item=fake_db.ItemTemplate.get(name='Mooncloth Bag'))
    player.bags()[2].item = fake_db.Container.New(base_item=fake_db.ItemTemplate.get(name='Mooncloth Bag'))
    player.bags()[3].item = fake_db.Container.New(base_item=fake_db.ItemTemplate.get(name='Mooncloth Bag'))

    client_pkt = packet.ClientAutoEquipItem.parse(
        packet.ClientAutoEquipItem.build(dict(
            container_slot=255,
            item_slot=enums.InventorySlots.BACKPACK_START + 15,
        )))

    mock_session = mock.MagicMock()
    mock_session.player_id = player.id

    response_pkts = handler.handler(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = inventory_change_failure.ServerInventoryChangeFailure.parse(response_bytes)
    assert response_op == op_code.Server.INVENTORY_CHANGE_FAILURE
    assert response_pkt.code == enums.InventoryChangeError.BAG_FULL


def test_handle_auto_equip_item_without_equipment_slot(mocker, fake_db):
    # Setup database.
    account = fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')
    realm = fake_db.Realm(name='r1', hostport='r1')
    player = fake_db.Player.New(
        id=10,
        account=account,
        realm=realm,
        name='c4',
        race=fake_db.ChrRaces[enums.EChrRaces.HUMAN],
        class_=fake_db.ChrClasses[enums.EChrClasses.WARRIOR],
        gender=enums.Gender.MALE,
    )

    player.backpack()[15].item = fake_db.Item.New(base_item=fake_db.ItemTemplate.get(name='Elementals Deck'))

    client_pkt = packet.ClientAutoEquipItem.parse(
        packet.ClientAutoEquipItem.build(dict(
            container_slot=255,
            item_slot=enums.InventorySlots.BACKPACK_START + 15,
        )))

    mock_session = mock.MagicMock()
    mock_session.player_id = player.id

    orm.flush()
    response_pkts = handler.handler(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = inventory_change_failure.ServerInventoryChangeFailure.parse(response_bytes)
    assert response_op == op_code.Server.INVENTORY_CHANGE_FAILURE
    assert response_pkt.code == enums.InventoryChangeError.NO_EQUIPMENT_SLOT_AVAILABLE
