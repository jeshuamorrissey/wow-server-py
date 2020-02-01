import logging
import select
import socketserver
from typing import Any, Tuple


class State:
    """State is a comment set of variables for all servers."""
    def __init__(self, log: logging.LoggerAdapter):
        """Create a state.

        Args:
            log: The logger to use.
        """
        self.log = log


class Session(socketserver.BaseRequestHandler):
    """Session represents a single client-server connection.

    The responsibilty of the Session object is to manage sending and
    receiving packets from the user and calling their appropriate
    handler functions.
    """
    StateType = State

    def setup(self):
        """Setup the session state."""
        self.state = self.StateType(log=self.server.log)

    def recv_header(self) -> Tuple[int, int]:
        """Receive the header from the request stream.

        Returns:
            A tuple of (op_code, data_len).
        """
        raise NotImplementedError()

    def write_response_header(self, op_code: Any, data: bytes) -> bytes:
        """Write the response header for the given data block.

        Args:
            op_code: The operation to write the header for.
            data: The data bytes generated for the packet.

        Returns:
            The header to be prepended to the data bytes.
        """
        raise NotImplementedError()

    def handle(self):
        """Handle the long-lived connection.

        Will receive packets one at a time (using recv_header()) and respond
        to them based on the handlers in self.server.handlers.
        """
        while True:
            op_code, data_len = self.recv_header()
            if op_code is None:
                self.state.log.debug('client disconnect')
                return

            self.state.log.debug(f'<-- {op_code.name}')
            data = self.request.recv(data_len)
            if data == b'' or op_code is None:
                self.state.log.debug('client disconnect')
                return

            if len(data) != data_len:
                self.state.log.warn(
                    f'Short read, wanted {data_len}, got {len(data)}')
                continue

            pkt_format = self.server.packet_formats.get(op_code, None)
            if not pkt_format:
                self.state.log.warning(
                    f'Unknown packet format for {op_code.name}')
                continue

            handler = self.server.handlers.get(op_code, None)
            if not handler:
                self.state.log.warning(f'Unhandled opcode {op_code.name}')
                continue

            responses = handler(pkt_format.parse(data), self.state)
            for op_code, response in responses:
                self.state.log.debug(f'--> {op_code.name}')
                header = self.write_response_header(op_code, response)
                self.request.sendall(header + response)
