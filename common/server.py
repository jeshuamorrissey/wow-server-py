import logging
import socketserver
from typing import Any, Callable, Dict, Text, Type

import coloredlogs
from construct import Struct


class Server(socketserver.TCPServer):
    def __init__(self, packet_formats: Dict[Any, Struct],
                 handlers: Dict[Any, Callable], log: logging.LoggerAdapter,
                 *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)

        self.packet_formats = packet_formats
        self.handlers = handlers
        self.log = log


def run(name: Text, host: Text, port: int, session_type: Type,
        packet_formats: Dict[Any, Struct], handlers: Dict[Any, Callable]):
    """Run a threaded socket server.

    This will take control of the current thread.

    Args:
        name: The name to give to the server's logger.
        host: The hostname to run the server on.
        port: The port to run the server on.
        session_type: The session request handler type to use.
        packet_formats: A mapping from OpCode --> construct.Struct.
        handlers: A mapping from OpCode --> handler function.
    """
    logger = logging.Logger(name=name)
    log_adapter = logging.LoggerAdapter(logger=logger, extra={})
    coloredlogs.install(level='DEBUG', logger=logger)

    Server.allow_reuse_address = True
    with Server(packet_formats=packet_formats,
                handlers=handlers,
                log=log_adapter,
                server_address=(host, port),
                RequestHandlerClass=session_type) as server:
        server.log.info(  # type: ignore
            f'Serving {name} server @ {host}:{port}...')
        server.serve_forever()
