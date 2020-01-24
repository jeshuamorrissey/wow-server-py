import logging
import socketserver

from database.account import Account
from login_server import op_code, router


class State:
    def __init__(self):
        self.account: Account = None
        self.b: int = None
        self.B: int = None


class Session(socketserver.BaseRequestHandler):
    def setup(self):
        self.state = State()

    def handle(self):
        while True:
            # TODO(jeshua): make this receive the exact size based on the opcode.
            data = self.request.recv(1024)
            if not data:
                logging.debug('client disconnect')
                return

            op = op_code.Client(data[0])
            logging.debug(f'<-- {op.name}')
            pkt_format = router.ClientPacket.Get(op)
            if not pkt_format:
                logging.error(f'Unknown packet format for {op.name}')
                return

            handler = router.Handler.Get(op)
            if not handler:
                logging.warning(f'Unhandled opcode {op.name}')
                return

            responses = handler(pkt_format.parse(data), self.state)
            for response in responses:
                op = op_code.Client(response[0])
                logging.debug(f'--> {op.name}')
                self.request.sendall(response)
