import enum
from typing import Any, Tuple

import pytest
from construct import Int8ul, Struct

from login_server import op_code, session


class FakeSession(session.Session):

    def __init__(self, mocker):
        super(FakeSession, self).__init__(request=mocker.MagicMock(), client_address='fake', server=mocker.MagicMock())

    def handle(self, run=False):
        if run:
            super(FakeSession, self).handle()


def test_read_header_short_read(mocker):
    session = FakeSession(mocker)
    session.request.recv.return_value = b''

    op, size = session.read_header()

    assert op is None
    assert size == 0
    assert session.request.recv.mock_calls == [mocker.call(1)]


def test_read_header(mocker):
    session = FakeSession(mocker)
    session.request.recv.return_value = op_code.Client.REALMLIST.to_bytes(1, 'little')

    op, length = session.read_header()

    assert op == op_code.Client.REALMLIST
    assert length == 4
    assert session.request.recv.mock_calls == [mocker.call(1)]


def test_read_header_login_challenge(mocker):
    session = FakeSession(mocker)

    values = iter([
        op_code.Client.LOGIN_CHALLENGE.to_bytes(1, 'little'),
        b'\x00\x01\x00',
    ])

    def _fake_recv(n):
        return next(values)

    session.request.recv.side_effect = _fake_recv

    op, length = session.read_header()

    assert op == op_code.Client.LOGIN_CHALLENGE
    assert length == 1
    assert session.request.recv.mock_calls == [mocker.call(1), mocker.call(3)]


def test_read_header_login_challenge_invalid(mocker):
    session = FakeSession(mocker)

    values = iter([
        op_code.Client.LOGIN_CHALLENGE.to_bytes(1, 'little'),
        b'\x00',
    ])

    def _fake_recv(n):
        return next(values)

    session.request.recv.side_effect = _fake_recv

    op, length = session.read_header()

    assert op is None
    assert length == 0
    assert session.request.recv.mock_calls == [mocker.call(1), mocker.call(3)]


def test_write_header(mocker):
    session = FakeSession(mocker)
    header = session.write_header(op_code.Server.LOGIN_CHALLENGE, b'data')
    assert header == b'\x00'


def test_write_header_realmlist(mocker):
    session = FakeSession(mocker)
    header = session.write_header(op_code.Server.REALMLIST, b'data')
    assert header == b'\x10\x04\x00'
