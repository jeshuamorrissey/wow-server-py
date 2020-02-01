from typing import Optional, Tuple

from common import session, srp
from world_server import op_code
from world_server.packets import auth_challenge


class Session(session.Session):
    def setup(self):
        super(Session, self).setup()

        # The currently logged in user's session key.
        self.session_key = bytearray()

        # Initial seed to prove login.
        self.auth_challenge_seed = 0

        # Packet counters used to encrypt/decrypt the header.
        self._send_i = self._send_j = 0
        self._recv_i = self._recv_j = 0

    def _decode_header(self, header: bytearray) -> bytearray:
        """Decode the client packet header."""
        for i in range(len(header)):
            self._recv_i %= len(self.session_key)
            x = (header[i] - self._recv_j) ^ self.session_key[self._recv_i]
            self._recv_i += 1
            self._recv_j = header[i]
            x %= 256
            header[i] = x

        return header

    def _encode_header(self, header: bytearray) -> bytearray:
        """Encode the server packet header."""
        for i in range(len(header)):
            self._send_i %= len(self.session_key)
            x = (header[i] ^ self.session_key[self._send_i]) + self._send_j
            self._send_i += 1
            x %= 256
            header[i] = self._send_j = x

        return header

    def read_header(self) -> Tuple[Optional[op_code.Client], int]:
        """Read the WORLD client packet header.

        This is always at least:
            2 byte length (including op_code)
            4 byte op_code

        ... but, if logged in, the header is encoded based on the number of
            packets which have been sent and received.

        Returns:
            The op_code + the length of the packet. op_code will be None
            in the case that the client disconnected.
        """
        header = bytearray(self.request.recv(6))
        if len(header) != 6:
            return (None, 0)

        # If they are authenticated, then decode the header.
        if self.session_key:
            header = self._decode_header(header)

        length = int.from_bytes(header[0:2], 'big') - 4
        op = op_code.Client(int.from_bytes(header[2:6], 'little'))
        return (op, length)

    def write_header(self, op: op_code.Server, data: bytes) -> bytes:
        """Write the AUTH server header.

        This is always at least:
            2 byte length (including op_code)
            2 byte op_code

        ... but, if logged in, the header is encoded based on the number of
            packets which have been sent and received.

        Returns:
            The header of the server packet.
        """
        length = int(len(data) + 2).to_bytes(2, 'big')
        header = length + op.to_bytes(2, 'little')

        # If they are authenticated, encode the header.
        if self.session_key:
            self._encode_header(header)

        return header

    def handle(self):
        """Send an initial AUTH_CHALLENGE packet when starting."""
        self.auth_challenge_seed = srp.Random(4)
        pkt = auth_challenge.ServerAuthChallenge.build(
            dict(seed=self.auth_challenge_seed))
        self.send_packet(op_code.Server.AUTH_CHALLENGE, pkt)

        # Continue to handle requests like normal.
        super(Session, self).handle()
