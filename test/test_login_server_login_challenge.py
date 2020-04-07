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
from login_server.handlers.login_challenge import handle_login_challenge
from login_server.packets.login_challenge import (ClientLoginChallenge, ServerLoginChallenge)


@pytest.mark.parametrize('account_name,expected_error', [
    ('account_exists', enums.LoginErrorCode.OK),
    ('account_does_not_exist', enums.LoginErrorCode.UNKNOWN_ACCOUNT),
])
def test_handle_login_challenge(account_name: Text, expected_error: enums.LoginErrorCode, fake_db):
    fake_db.Account(name='account_exists', salt_str='11', verifier_str='22')

    client_pkt = ClientLoginChallenge.parse(
        ClientLoginChallenge.build(
            dict(
                game_name='GAME',
                version_major=1,
                version_minor=2,
                version_bug=3,
                build=4,
                platform='PLAT',
                os='OSOS',
                locale='TEST',
                timezone_offset=5,
                ip_address=6,
                account_name=account_name,
            )))

    mock_session = mock.MagicMock()
    response_pkts = handle_login_challenge(client_pkt, mock_session)

    assert 1 == len(response_pkts)
    assert op_code.Server.LOGIN_CHALLENGE == response_pkts[0][0]

    response = ServerLoginChallenge.parse(response_pkts[0][1])
    assert expected_error == response.error

    if expected_error == enums.LoginErrorCode.OK:
        assert mock_session.account_name == account_name
        assert mock_session.b is not None
        assert mock_session.B == response.challenge.B


if __name__ == '__main__':
    sys.exit(pytest.main([__file__]))
