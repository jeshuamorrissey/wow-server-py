import argparse
import enum
import os
import threading
from typing import Text

import coloredlogs
from pony import orm

import login_server.handlers  # register handlers
import login_server.packets  # register packet formats
from common import server
from database import common
from database.account import Account
from database.db import db
from database.realm import Realm
from login_server import router as login_router
from login_server import session as login_session


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
        Account.New(username='jeshua', password='jeshua')
        Realm(name='Brisbane', hostport=f'{world_host}:{world_port}')


def main(args: argparse.Namespace):
    # Load the database.
    setup_db(args.db_file, args.host, args.world_port)

    # Create the packet handling threads.
    server.run(
        name='AUTH',
        host=args.host,
        port=args.auth_port,
        session_type=login_session.Session,
        packet_formats=login_router.LoginClientPacket.ROUTES,
        handlers=login_router.LoginHandler.ROUTES,
    )


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
