import argparse
import logging
import socketserver
import tempfile

import coloredlogs
import sqlitedict

import login_server.handlers  # register all of the handlers
import login_server.packets  # register all of the packets
from database import db
from database.account import Account
from login_server import session, srp


def setup_db():
    salt = srp.Random(32)
    db[Account.Key('JESHUA')] = Account(
        name='JESHUA',
        salt=salt,
        verifier=srp.GenerateVerifier('JESHUA', 'JESHUA', salt),
    )

    db.commit()


def main(args: argparse.Namespace):
    setup_db()
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((args.host, args.port),
                                session.Session) as server:
        logging.info(f'Serving AUTH server @ {args.host}:{args.port}...')
        server.serve_forever()


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(
        description='Server to handle the initial login connection.')
    argument_parser.add_argument('--port',
                                 type=int,
                                 default=6000,
                                 help='The port to list for connections on.')
    argument_parser.add_argument('--host',
                                 type=str,
                                 default='localhost',
                                 help='The host to list for connections on.')
    coloredlogs.install(level='DEBUG')

    main(argument_parser.parse_args())
