import enum
from typing import Any, Tuple

from construct import Int8ul, Struct

from common import session

FakePacket = Struct('num' / Int8ul)


class AnyStringWith(str):

    def __eq__(self, other):
        return self in other


class FakeOpCode(enum.IntEnum):
    OP1 = 1
    OP2 = 2


class FakeSession(session.Session):

    def __init__(self, mocker):
        super(FakeSession, self).__init__(request=mocker.MagicMock(), client_address='fake', server=mocker.MagicMock())

    def setup(self):
        super(FakeSession, self).setup()

        self.read_headers = []
        self.write_headers = []

    def handle(self, run=False):
        if run:
            super(FakeSession, self).handle()

    def write_header(self, op: Any, data: bytes) -> bytes:
        if not self.write_headers:
            return b''
        return self.write_headers.pop(0).format(op=op, data=data.decode()).encode()

    def read_header(self) -> Tuple[int, int]:
        if not self.read_headers:
            return (None, 0)
        return self.read_headers.pop(0)


def test_handle_client_disconnect_no_packet(mocker):
    session = FakeSession(mocker)

    session.handle(run=True)

    session.log.warning.assert_called_once_with('client disconnect')
    assert session.request.recv.call_count == 0


def test_handle_client_disconnect_when_reading_packet(mocker):
    session = FakeSession(mocker)
    session.read_headers.append((FakeOpCode.OP1, 100))
    session.request.recv.return_value = b''

    session.handle(run=True)

    session.log.warning.assert_called_once_with('client disconnect')
    session.request.recv.assert_called_once_with(100)


def test_handle_short_read(mocker):
    session = FakeSession(mocker)
    session.read_headers.append((FakeOpCode.OP1, 4))
    session.request.recv.return_value = b'123'

    session.handle(run=True)

    session.log.warning.assert_has_calls([
        mocker.call(AnyStringWith('short read')),
        mocker.call('client disconnect'),
    ])


def test_handle_unknown_packet_format(mocker):
    session = FakeSession(mocker)
    session.read_headers.append((FakeOpCode.OP1, 4))
    session.request.recv.return_value = b'1234'

    session.server.packet_formats = {}
    session.server.handlers = {}

    session.handle(run=True)

    session.log.warning.assert_has_calls([
        mocker.call(AnyStringWith('unknown packet format')),
        mocker.call('client disconnect'),
    ])


def test_handle_unhandled_opcode(mocker):
    session = FakeSession(mocker)
    session.read_headers.append((FakeOpCode.OP1, 4))
    session.request.recv.return_value = b'1234'

    session.server.packet_formats = {FakeOpCode.OP1: FakePacket}
    session.server.handlers = {}

    session.handle(run=True)

    session.log.warning.assert_has_calls([
        mocker.call(AnyStringWith('unhandled opcode')),
        mocker.call('client disconnect'),
    ])


def test_handle_single_response(mocker):
    session = FakeSession(mocker)
    session.read_headers.append((FakeOpCode.OP1, 1))
    session.write_headers.append('header({op})data({data})01')
    session.write_headers.append('header({op})data({data})02')
    session.request.recv.return_value = b'\xFF'

    def _fake_handler(pkt, session_):
        assert pkt.num == 255
        assert session == session_

        return [
            (FakeOpCode.OP2, b'resp1'),
            (FakeOpCode.OP2, b'resp2'),
        ]

    session.server.packet_formats = {FakeOpCode.OP1: FakePacket}
    session.server.handlers = {FakeOpCode.OP1: _fake_handler}

    session.handle(run=True)

    session.request.sendall.assert_has_calls([
        mocker.call(b'header(2)data(resp1)01resp1'),
        mocker.call(b'header(2)data(resp2)02resp2'),
    ])
    session.log.warning.assert_has_calls([
        mocker.call('client disconnect'),
    ])
