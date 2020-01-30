import argparse
import threading
from typing import Text

import coloredlogs
from pony import orm

import login_server.handlers  # register handlers
import login_server.packets  # register packet formats
from common import server
from database.account import Account
from database.db import db
from login_server import router as login_router
from login_server import session as login_session


def setup_db(db_file: Text):
    # Connect to SQLite in memory.
    db.bind(provider='sqlite', filename=db_file, create_db=True)
    db.generate_mapping(create_tables=True)

    # Generate some test data.
    with orm.db_session:
        if not Account['JESHUA']:
            Account.New(username='jeshua', password='jeshua')


def main(args: argparse.Namespace):
    # Load the database.
    setup_db(args.db_file)

    # Create the packet handling threads.
    auth_thread = threading.Thread(
        name='auth-server',
        target=server.run,
        kwargs=dict(name='AUTH',
                    host=args.host,
                    port=args.auth_port,
                    session_type=login_session.Session,
                    packet_formats=login_router.LoginClientPacket.ROUTES,
                    handlers=login_router.LoginHandler.ROUTES))

    # Start the threads.
    auth_thread.start()

    # Wait for them to finish.
    auth_thread.join()


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(
        description='Server to handle the initial login connection.')
    argument_parser.add_argument(
        '--auth_port',
        type=int,
        default=6000,
        help='The port to list for AUTH connections on.')
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
