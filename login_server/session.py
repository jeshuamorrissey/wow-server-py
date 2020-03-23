from typing import Optional, Tuple

from common import session
from login_server import op_code

# Mapping of packet --> output packet size, for the constant-sized packets.
# This is necessary because most packets don't include the length by
# default.
_OP_PACKET_SIZE = {
    op_code.Client.LOGIN_PROOF: 74,
    op_code.Client.REALMLIST: 4,
}


class Session(session.Session):

    def setup(self):
        super(Session, self).setup()

        # The currently logged in account.
        self.account_name: str = None

        # The public/private, generated ephemeral values for SRP.
        self.b: int = None
        self.B: int = None

    def read_header(self) -> Tuple[Optional[int], int]:
        """Read the AUTH client packet header.

        This is always at least:
            1 byte op_code

        ... but for LOGIN_CHALLENGE, also includes:
            1 byte error (unknown usage)
            2 byte length

        Returns:
            The op_code + the length of the packet. op_code will be None
            in the case that the client disconnected.
        """
        header = self.request.recv(1)
        if len(header) != 1:
            return None, 0

        op = op_code.Client(int.from_bytes(header, 'little'))
        length = _OP_PACKET_SIZE.get(op, 1024)

        # Special case: LOGIN_CHALLENGE includes a length.
        if op == op_code.Client.LOGIN_CHALLENGE:
            extended_header = self.request.recv(3)
            if len(extended_header) != 3:
                return None, 0

            length = int.from_bytes(extended_header[1:], 'little')

        return op, length

    def write_header(self, op: op_code.Server, data: bytes) -> bytes:
        """Write the AUTH server header.

        This is always at least:
            1 byte op_code

        ... but for REALMLIST, also includes:
            2 byte length

        Returns:
            The header of the server packet.
        """
        header = op.to_bytes(1, 'little')
        if op == op_code.Server.REALMLIST:
            header += len(data).to_bytes(2, 'little')

        return header
