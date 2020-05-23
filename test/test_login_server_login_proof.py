import enum
import io
import logging
import sys
import unittest
from typing import Text
from unittest import mock

import pytest

from database import enums
from login_server import op_code
from login_server.handlers import login_proof as handler
from login_server.packets import login_proof as packet


def test_handle_login_proof_invalid_session(fake_db):
    client_pkt = packet.ClientLoginProof.parse(
        packet.ClientLoginProof.build(dict(
            A=1,
            M=2,
            crc_hash=3,
            number_of_keys=4,
            security_flags=5,
        )))

    mock_session = mock.MagicMock()
    mock_session.account_name = None

    response_pkts = handler.handle_login_proof(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerLoginProof.parse(response_bytes)
    assert response_op == op_code.Server.LOGIN_PROOF
    assert response_pkt.error == enums.LoginErrorCode.FAILED


def test_handle_login_proof_invalid_password(mocker, fake_db):
    mock_srp = mocker.patch.object(handler, 'srp')

    fake_db.Account(name='account', salt_str='11', verifier_str='22')

    client_pkt = packet.ClientLoginProof.parse(
        packet.ClientLoginProof.build(dict(
            A=1,
            M=2,
            crc_hash=3,
            number_of_keys=4,
            security_flags=5,
        )))

    mock_session = mock.MagicMock()
    mock_session.account_name = 'account'
    mock_session.b = 1
    mock_session.B = 2

    mock_srp.CalculateSessionKey.return_value = (0, 1)

    response_pkts = handler.handle_login_proof(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerLoginProof.parse(response_bytes)
    assert response_op == op_code.Server.LOGIN_PROOF
    assert response_pkt.error == enums.LoginErrorCode.UNKNOWN_ACCOUNT


def test_handler_login_proof(mocker, fake_db):
    mock_srp = mocker.patch.object(handler, 'srp')

    fake_db.Account(name='account', salt_str='11', verifier_str='22')

    client_pkt = packet.ClientLoginProof.parse(
        packet.ClientLoginProof.build(dict(
            A=1,
            M=2,
            crc_hash=3,
            number_of_keys=4,
            security_flags=5,
        )))

    mock_session = mock.MagicMock()
    mock_session.account_name = 'account'
    mock_session.b = 1
    mock_session.B = 2

    mock_srp.CalculateSessionKey.return_value = (1, 2)
    mock_srp.CalculateServerProof.return_value = 1

    response_pkts = handler.handle_login_proof(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerLoginProof.parse(response_bytes)
    assert response_op == op_code.Server.LOGIN_PROOF
    assert response_pkt.error == enums.LoginErrorCode.OK
    assert response_pkt.proof.proof == 1
    assert fake_db.Account.get(name='account').session_key_str == '1'
