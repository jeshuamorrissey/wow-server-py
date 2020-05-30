import socketserver
from typing import Any, Tuple


class Session(socketserver.BaseRequestHandler):
    """Session represents a single client-server connection.

    The responsibilty of the Session object is to manage sending and
    receiving packets from the user and calling their appropriate
    handler functions.
    """

    def setup(self):
        """Setup the session with some common infrastructure.

        This will add the following members:
            log: A logger which is specific to this session.
        """
        super(Session, self).setup()

        self.log = self.server.log

    def send_packet(self, op: Any, data: bytes):
        """Send a data packet.

        This will first generate the response header, prepend it to the packet
        and then send it back to the client.

        Args:
            op: The op_code for this packet.
            data: The raw contents of the packet.
        """
        self.log.debug(f'--> {op.name}')
        header = self.write_header(op, data)
        self.request.sendall(header + data)

    def read_header(self) -> Tuple[int, int]:
        """Read the header from the request stream.

        Returns:
            A tuple of (op_code, data_len).
        """
        raise NotImplementedError()

    def handle(self):
        """Handle the long-lived connection.

        Will receive packets one at a time (using read_header()) and respond
        to them based on the handlers in self.server.handlers.
        """
        while True:
            op_code, data_len = self.read_header()
            if op_code is None:
                self.log.warning('client disconnect')
                return

            self.log.debug(f'<-- {op_code.name}')
            if data_len > 0:
                data = self.request.recv(data_len)
                if data == b'' or op_code is None:
                    self.log.warning('client disconnect')
                    return
            else:
                data = b''

            if len(data) != data_len:
                self.log.warning(f'short read, wanted {data_len}, got {len(data)}')
                continue

            pkt_format = self.server.packet_formats.get(op_code, None)
            if not pkt_format:
                self.log.warning(f'unknown packet format for {op_code.name}')
                continue

            handler = self.server.handlers.get(op_code, None)
            if not handler:
                self.log.warning(f'unhandled opcode {op_code.name}')
                continue

            responses = handler(pkt_format.parse(data), self)
            for op, response in responses:
                self.send_packet(op, response)

    def write_header(self, op: Any, data: bytes) -> bytes:
        """Write the response header for the given data block.

        Args:
            op: The op_code to write the header for.
            data: The data bytes generated for the packet.

        Returns:
            The header to be prepended to the data bytes.
        """
        raise NotImplementedError()
