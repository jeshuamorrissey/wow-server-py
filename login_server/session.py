import logging
import socketserver

from login_server import op_code, router


class Session(socketserver.BaseRequestHandler):
    def setup(self):
        self.state = {}

    def handle(self):
        # TODO(jeshua): make this receive the exact size based on the opcode.
        data = self.request.recv(1024).strip()

        op = op_code.Client(data[0])
        pkt_format = router.ClientPacket.Get(op)
        if not pkt_format:
            logging.error(f'Unknown packet format for opcode {op}')
            return

        handler = router.Handler.Get(op)
        if not handler:
            logging.warning(f'Unhandled opcode {op}')
            return

        responses = handler(pkt_format.parse(data), self.state)
        for response in responses:
            print(response)
            self.request.send(response)
