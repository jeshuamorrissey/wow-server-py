from typing import Tuple, Optional

from common import session
from login_server import op_code

_OP_PACKET_SIZE = {
    op_code.Client.LOGIN_PROOF: 74,
    op_code.Client.REALMLIST: 4,
}


class State(session.State):
    def __init__(self, *args, **kwargs):
        super(State, self).__init__(*args, **kwargs)

        self.account_name: str = None
        self.b: int = None
        self.B: int = None


class Session(session.Session):
    StateType = State

    def recv_header(self) -> Tuple[Optional[int], int]:
        header = self.request.recv(1)
        if header == b'':
            return None, 0

        op = op_code.Client(int.from_bytes(header, 'little'))
        if op == op_code.Client.LOGIN_CHALLENGE:
            extended_header = self.request.recv(3)
            return op, int.from_bytes(extended_header[1:], 'little')
        return op, _OP_PACKET_SIZE.get(op, 1024)

    def write_response_header(self, op: op_code.Server, data: bytes) -> bytes:
        header = op.to_bytes(1, 'little')
        if op == op_code.Server.REALMLIST:
            header += len(data).to_bytes(2, 'little')

        return header
