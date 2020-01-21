import argparse
import logging
import socketserver
import tempfile
import sqlitedict

import login_server.handlers  # register all of the handlers
import login_server.packets  # register all of the packets
from login_server import db, session, srp


def setup_db(db: sqlitedict.SqliteDict):
    salt = srp.Random(32)
    db['account::jeshua'] = {
        'account_name': 'jeshua',
        'salt': salt,
        'verifier': srp.GenerateVerifier('JESHUA', 'JESHUA', salt),
    }

    db.commit()


def main(args: argparse.Namespace):
    with sqlitedict.SqliteDict(args.db_file) as sqlite_db:
        setup_db(sqlite_db)
        db.db = sqlite_db

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
    argument_parser.add_argument('--db_file',
                                 type=str,
                                 default='/tmp/wow.db',
                                 help='The file to use for the game database.')
    logging.getLogger().setLevel(logging.DEBUG)

    main(argument_parser.parse_args())
