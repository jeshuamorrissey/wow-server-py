"""Utility to build base Python files for defining packets."""

import argparse
import os
import sys
from typing import Text

from world_server import op_code

_SERVER_PACKET_FORMAT = '''from construct import Int32ul, Struct

Server{op_camel_case} = Struct(
    'id' / Int32ul,
    'id2' / Int32ul,
)
'''

_CLIENT_PACKET_FORMAT = '''from construct import Int32ul, Struct

from world_server import op_code, router

Client{op_camel_case} = router.ClientPacket.Register(
    op_code.Client.{op_name},
    Struct(
        'id' / Int32ul,
        'field' / Int32ul,
    ),
)
'''

_CLIENT_SERVER_PACKET_FORMAT = '''from construct import Int32ul, Struct

from world_server import op_code, router

Client{op_camel_case} = router.ClientPacket.Register(
    op_code.Client.{op_name},
    Struct(
        'id' / Int32ul,
        'field' / Int32ul,
    ),
)

Server{op_camel_case} = Struct(
    'id' / Int32ul,
    'id2' / Int32ul,
)
'''

_CLIENT_HANDLER_FORMAT = '''from typing import List, Tuple

from pony import orm

from world_server import op_code, router, session
from world_server.packets import {op_packet_file}


@router.Handler(op_code.Client.{op_name})
@orm.db_session
def handler(pkt: {op_packet_file}.Client{op_camel_case},
            session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    return []
'''

_CLIENT_SERVER_HANDLER_FORMAT = '''from typing import List, Tuple

from pony import orm

from world_server import op_code, router, session
from world_server.packets import {op_packet_file}


@router.Handler(op_code.Client.{op_name})
@orm.db_session
def handler(pkt: {op_packet_file}.Client{op_camel_case},
            session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    return [(
        op_code.Server.{op_name},
        {op_packet_file}.Server{op_camel_case}.build(dict()),
    )]
'''


def make_client_server_packet(
    output_path: Text,
    op_name: Text,
    op_camel_case: Text,
    op_packet_file: Text,
    op_packet_filename: Text,
):
    with open(os.path.join(output_path, 'packets', op_packet_filename), 'w') as f:
        f.write(_CLIENT_SERVER_PACKET_FORMAT.format(op_camel_case=op_camel_case, op_name=op_name))

    with open(os.path.join(output_path, 'handlers', op_packet_filename), 'w') as f:
        f.write(
            _CLIENT_SERVER_HANDLER_FORMAT.format(op_packet_file=op_packet_file,
                                                 op_camel_case=op_camel_case,
                                                 op_name=op_name))


def make_client_packet(
    output_path: Text,
    op_name: Text,
    op_camel_case: Text,
    op_packet_file: Text,
    op_packet_filename: Text,
):
    with open(os.path.join(output_path, 'packets', op_packet_filename), 'w') as f:
        f.write(_CLIENT_PACKET_FORMAT.format(op_camel_case=op_camel_case, op_name=op_name))

    with open(os.path.join(output_path, 'handlers', op_packet_filename), 'w') as f:
        f.write(
            _CLIENT_HANDLER_FORMAT.format(op_packet_file=op_packet_file, op_camel_case=op_camel_case, op_name=op_name))


def make_server_packet(
    output_path: Text,
    op_camel_case: Text,
    op_packet_filename: Text,
):
    with open(os.path.join(output_path, 'packets', op_packet_filename), 'w') as f:
        f.write(_SERVER_PACKET_FORMAT.format(op_camel_case=op_camel_case))


def main(output_path: Text, op_name: Text):
    client_values = {e.name for e in op_code.Client}
    server_values = {e.name for e in op_code.Server}

    op_packet_file = op_name.lower()
    op_packet_filename = f'{op_packet_file}.py'
    op_camel_case = ''.join([part.title() for part in op_name.split('_')])

    if op_name in client_values and op_name in server_values:
        make_client_server_packet(output_path, op_name, op_camel_case, op_packet_file, op_packet_filename)
    elif op_name in client_values:
        make_client_packet(output_path, op_name, op_camel_case, op_packet_file, op_packet_filename)
    elif op_name in server_values:
        make_server_packet(output_path, op_camel_case, op_packet_filename)
    else:
        print(f'Unknown opcode "{op_name}".')
        return 1

    return 0


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--output_path', type=str, required=True)
    arg_parser.add_argument('client_op_name', type=str)

    args = arg_parser.parse_args()
    sys.exit(main(args.output_path, args.client_op_name))
