import logging
import socketserver

from login_server import op_code, router


class Session(socketserver.BaseRequestHandler):
    def setup(self):
        self.state = {}

    def handle(self):
        while True:
            # TODO(jeshua): make this receive the exact size based on the opcode.
            data = self.request.recv(1024)
            if not data:
                logging.debug('client disconnect')
                return

            print(data)

            op = op_code.Client(data[0])
            logging.debug(f'<-- {op.name}')
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
                self.request.sendall(response)
