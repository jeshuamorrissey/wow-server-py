import argparse
import logging
import socketserver
import sys

from login_server import session
from login_server.packets import login_challenge


def main(args: argparse.Namespace):
    print(login_challenge.LoginChallenge.from_bytes(b'\x00\x01').error)
    with socketserver.ThreadingTCPServer((args.host, args.port),
                                         session.Session) as server:
        logging.info(f'Serving AUTH server @ {args.host}:{args.port}...')
        server.serve_forever()

    return 0


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

    logging.getLogger().setLevel(logging.DEBUG)
    sys.exit(main(argument_parser.parse_args()))
