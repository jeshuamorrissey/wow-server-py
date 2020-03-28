import enum
import io
import logging
import sys
import unittest
from typing import Text
from unittest import mock

import parameterized
import pytest

from database import data, enums
from world_server import op_code
from world_server.handlers import auth_session as handler
from world_server.packets import auth_response
from world_server.packets import auth_session as packet


def test_handle_auth_session(mocker, fake_db):
    # Setup database.
    fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')

    client_pkt = packet.ClientAuthSession.parse(
        packet.ClientAuthSession.build(
            dict(
                build_number=1234,
                account_name='account',
                client_seed=1000,
                client_proof=2000,
                addon_size=0,
                addons=b'',
            )))

    mock_srp = mocker.patch.object(handler, 'srp')
    mock_srp.CalculateAuthSessionProof.return_value = 2000

    mock_session = mock.MagicMock()
    mock_session.auth_challenge_seed = 1

    response_pkts = handler.handle_auth_session(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = auth_response.ServerAuthResponse.parse(response_bytes)
    assert response_op == op_code.Server.AUTH_RESPONSE
    assert auth_response.ErrorCode.OK == auth_response.ErrorCode(response_pkt.error)


def test_handle_auth_session_invalid_proof(mocker, fake_db):
    # Setup database.
    fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')

    client_pkt = packet.ClientAuthSession.parse(
        packet.ClientAuthSession.build(
            dict(
                build_number=1234,
                account_name='account',
                client_seed=1000,
                client_proof=2000,
                addon_size=0,
                addons=b'',
            )))

    mock_srp = mocker.patch.object(handler, 'srp')
    mock_srp.CalculateAuthSessionProof.return_value = 2001

    mock_session = mock.MagicMock()
    mock_session.auth_challenge_seed = 1

    response_pkts = handler.handle_auth_session(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = auth_response.ServerAuthResponse.parse(response_bytes)
    assert response_op == op_code.Server.AUTH_RESPONSE
    assert auth_response.ErrorCode.FAILED == auth_response.ErrorCode(response_pkt.error)


def test_handle_auth_session_unknown_account(mocker, fake_db):
    # Setup database.
    fake_db.Account(name='account', salt_str='11', verifier_str='22', session_key_str='33')

    client_pkt = packet.ClientAuthSession.parse(
        packet.ClientAuthSession.build(
            dict(
                build_number=1234,
                account_name='invalid',
                client_seed=1000,
                client_proof=2000,
                addon_size=0,
                addons=b'',
            )))

    mock_srp = mocker.patch.object(handler, 'srp')
    mock_srp.CalculateAuthSessionProof.return_value = 2001

    mock_session = mock.MagicMock()
    mock_session.auth_challenge_seed = 1

    response_pkts = handler.handle_auth_session(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = auth_response.ServerAuthResponse.parse(response_bytes)
    assert response_op == op_code.Server.AUTH_RESPONSE
    assert auth_response.ErrorCode.UNKNOWN_ACCOUNT == auth_response.ErrorCode(response_pkt.error)


if __name__ == '__main__':
    sys.exit(pytest.main([__file__]))
