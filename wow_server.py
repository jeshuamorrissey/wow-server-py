import argparse
import enum
import logging
import os
import threading
from typing import Text

import coloredlogs
from pony import orm

import login_server.handlers  # register handlers
import login_server.packets  # register packet formats
import world_server.handlers  # register handlers
import world_server.packets  # register packet formats
from common import server
from database import common
from database.db import db
from database.dbc import constants as c
from database.dbc import data
from database.dbc.chr_start_locations import ChrStartLocation
from database.dbc.item_template import ItemTemplate
from database.world.account import Account
from database.world.game_object.item import Item
from database.world.game_object.player import Player, EquippedItem
from database.world.guild import Guild
from database.world.realm import Realm
from login_server import router as login_router
from login_server import session as login_session
from world_server import router as world_router
from world_server import session as world_session


def setup_db(args: argparse.Namespace):
    # TODO(jeshua): make the DB persistant.
    # Clear the DB for testing.
    if args.reset_database and os.path.exists(args.db_file):
        os.remove(args.db_file)

    # Connect to SQLite in memory.
    db.bind(provider='sqlite', filename=args.db_file, create_db=True)
    db.provider.converter_classes.append((enum.Enum, common.EnumConverter))
    db.generate_mapping(create_tables=True)

    # Clear the world database tables so they can be created again.
    if args.reset_world_database:
        with orm.db_session:
            db.execute('DELETE FROM Account')
            db.execute('DELETE FROM Realm')
            db.execute('DELETE FROM Guild')
            db.execute('DELETE FROM GameObject')
            db.execute('DELETE FROM EquippedItem')

    # Load DBC data.
    if args.reset_database:
        data.LoadDBC()

    # Generate some test data.
    with orm.db_session:
        account = Account.New(username='jeshua', password='jeshua')
        realm = Realm(name='Brisbane',
                      hostport=f'{args.host}:{args.world_port}')
        guild = Guild()
        Player.New(
            account=account,
            realm=realm,
            name='Jeshua',
            race=c.Race.HUMAN,
            class_=c.Class.HUNTER,
            gender=c.Gender.MALE,
            guild=guild,
        )

        sasha = Player.New(
            account=account,
            realm=realm,
            name='Sasha',
            race=c.Race.HUMAN,
            class_=c.Class.WARRIOR,
            gender=c.Gender.FEMALE,
        )

        EquippedItem(
            owner=sasha,
            slot=c.EquipmentSlot.MAIN_HAND,
            item=Item(base=ItemTemplate.get(
                name='Thunderfury, Blessed Blade of the Windseeker')),
        )

        EquippedItem(
            owner=sasha,
            slot=c.EquipmentSlot.OFF_HAND,
            item=Item(base=ItemTemplate.get(
                name='Ancient Cornerstone Grimoire')),
        )

        EquippedItem(
            owner=sasha,
            slot=c.EquipmentSlot.BACK,
            item=Item(base=ItemTemplate.get(name='Cloak of the Necropolis')),
        )

        EquippedItem(
            owner=sasha,
            slot=c.EquipmentSlot.WAIST,
            item=Item(base=ItemTemplate.get(name='Frostfire Belt')),
        )

        EquippedItem(
            owner=sasha,
            slot=c.EquipmentSlot.WRISTS,
            item=Item(base=ItemTemplate.get(name='Frostfire Bindings')),
        )

        EquippedItem(
            owner=sasha,
            slot=c.EquipmentSlot.HEAD,
            item=Item(base=ItemTemplate.get(name='Frostfire Circlet')),
        )

        EquippedItem(
            owner=sasha,
            slot=c.EquipmentSlot.HANDS,
            item=Item(base=ItemTemplate.get(name='Frostfire Gloves')),
        )

        EquippedItem(
            owner=sasha,
            slot=c.EquipmentSlot.LEGS,
            item=Item(base=ItemTemplate.get(name='Frostfire Leggings')),
        )

        EquippedItem(
            owner=sasha,
            slot=c.EquipmentSlot.CHEST,
            item=Item(base=ItemTemplate.get(name='Frostfire Robe')),
        )

        EquippedItem(
            owner=sasha,
            slot=c.EquipmentSlot.FEET,
            item=Item(base=ItemTemplate.get(name='Frostfire Sandals')),
        )

        EquippedItem(
            owner=sasha,
            slot=c.EquipmentSlot.SHOULDERS,
            item=Item(base=ItemTemplate.get(name='Frostfire Shoulderpads')),
        )

        EquippedItem(
            owner=sasha,
            slot=c.EquipmentSlot.FINGER1,
            item=Item(base=ItemTemplate.get(name='Frostfire Ring')),
        )


def main(args: argparse.Namespace):
    # Load the database.
    setup_db(args)

    # Create the packet handling threads.
    auth_thread = threading.Thread(
        target=server.run,
        kwargs=dict(
            name='AUTH',
            host=args.host,
            port=args.auth_port,
            session_type=login_session.Session,
            packet_formats=login_router.ClientPacket.ROUTES,
            handlers=login_router.Handler.ROUTES,
        ))

    world_thread = threading.Thread(
        target=server.run,
        kwargs=dict(
            name='WORLD',
            host=args.host,
            port=args.world_port,
            session_type=world_session.Session,
            packet_formats=world_router.ClientPacket.ROUTES,
            handlers=world_router.Handler.ROUTES,
        ))

    auth_thread.start()
    world_thread.start()

    auth_thread.join()
    world_thread.join()


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(
        description='Server to handle the initial login connection.')
    argument_parser.add_argument(
        '--auth_port',
        type=int,
        default=5000,
        help='The port to list for AUTH connections on.')
    argument_parser.add_argument(
        '--world_port',
        type=int,
        default=5001,
        help='The port to list for WORLD connections on.')
    argument_parser.add_argument('--host',
                                 type=str,
                                 default='localhost',
                                 help='The host to list for connections on.')
    argument_parser.add_argument(
        '--db_file',
        type=str,
        default='/tmp/wow_server.db',
        help='The file to store the World database in.')
    argument_parser.add_argument(
        '--reset_database',
        action='store_true',
        help='If True, the DBC database will be reloaded.')
    argument_parser.add_argument(
        '--reset_world_database',
        action='store_true',
        help='If True, the World database will be reloaded.')
    argument_parser.set_defaults(reset_database=False,
                                 reset_world_database=True)
    coloredlogs.install(level='DEBUG')

    main(argument_parser.parse_args())
