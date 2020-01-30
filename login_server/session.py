from typing import Tuple, Optional

from common import session
from login_server import op_code


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
        op = op_code.Client(int.from_bytes(header, 'little'))

        if op == op_code.Client.LOGIN_CHALLENGE:
            extended_header = self.request.recv(3)
            return op, int.from_bytes(extended_header[1:], 'little')
        elif op == op_code.Client.LOGIN_PROOF:
            return op, 74

        return op, 1024
