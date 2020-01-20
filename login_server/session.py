import socketserver


class Session(socketserver.BaseRequestHandler):
    def handle(self):
        print(self.request.recv(1024).strip())
