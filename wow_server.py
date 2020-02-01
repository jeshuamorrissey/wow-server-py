import argparse
import enum
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
from database.account import Account
from database.db import db
from database.game_object.player import Player
from database.realm import Realm
from dbc import constants as c
from login_server import router as login_router
from login_server import session as login_session
from world_server import router as world_router
from world_server import session as world_session


def setup_db(db_file: Text, world_host: Text, world_port: int):
    # TODO(jeshua): make the DB persistant.
    # Clear the DB for testing.
    if os.path.exists(db_file):
        os.remove(db_file)

    # Connect to SQLite in memory.
    db.bind(provider='sqlite', filename=db_file, create_db=True)
    db.provider.converter_classes.append((enum.Enum, common.EnumConverter))
    db.generate_mapping(create_tables=True)

    # Generate some test data.
    with orm.db_session:
        account = Account.New(username='jeshua', password='jeshua')
        realm = Realm(name='Brisbane', hostport=f'{world_host}:{world_port}')

        # Make a character.
        Player(
            account=account,
            realm=realm,
            name='Jeshua',

            # GameObject attributes.
            level=1,
            race=c.Race.HUMAN,
            class_=c.Class.MAGE,
            gender=c.Gender.MALE,
            skin_color=0,
            face=0,
            hair_style=0,
            hair_color=0,
            feature=0,
        )


def main(args: argparse.Namespace):
    # Load the database.
    setup_db(args.db_file, args.host, args.world_port)

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
    argument_parser.add_argument('--db_file',
                                 type=str,
                                 default='/tmp/wow_server.db',
                                 help='The file to store the database in.')
    coloredlogs.install(level='DEBUG')

    main(argument_parser.parse_args())
