import enum
import io
import logging
import unittest
from test.fake_db import TestWithDatabase
from typing import Text
from unittest import mock

from pony import orm

from common import server, srp
from database import common, constants, enums, game, world
from database.db import db
from login_server import op_code, router
from login_server.handlers import constants as c
from login_server.handlers import login_challenge
from login_server.handlers.login_challenge import \
    handle_login_challenge as handler
from login_server.packets.login_challenge import (ClientLoginChallenge, ServerLoginChallenge)
from login_server.session import Session


class TestLoginChallenge(TestWithDatabase):

    @mock.patch.object(login_challenge, 'srp')
    def test_account_exists(self, mock_srp):
        with orm.db_session:
            world.Account(name='account', salt_str='11', verifier_str='22')

        mock_srp.GenerateEphemeral.return_value = (1, 2)
        mock_srp.Random.return_value = 1

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
                    account_name='account',
                )))

        mock_session = mock.MagicMock()
        response = handler(client_pkt, mock_session)

        self.assertEqual(1, len(response))
        self.assertEqual(op_code.Server.LOGIN_CHALLENGE, response[0][0])

        response_op, response_bytes = response[0]
        self.assertEqual(op_code.Server.LOGIN_CHALLENGE, response_op)

        response_pkt = ServerLoginChallenge.parse(response_bytes)
        self.assertEqual(c.LoginErrorCode.OK, response_pkt.error)
        self.assertEqual(2, response_pkt.challenge.B)
        self.assertEqual(11, response_pkt.challenge.salt)
        self.assertEqual('account', mock_session.account_name)
        self.assertEqual(1, mock_session.b)
        self.assertEqual(2, mock_session.B)

    def test_no_account(self):
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
                    account_name='account',
                )))

        mock_session = mock.MagicMock()
        response = handler(client_pkt, mock_session)

        self.assertEqual(1, len(response))
        self.assertEqual(op_code.Server.LOGIN_CHALLENGE, response[0][0])

        response_op, response_bytes = response[0]
        self.assertEqual(op_code.Server.LOGIN_CHALLENGE, response_op)

        response_pkt = ServerLoginChallenge.parse(response_bytes)
        self.assertEqual(c.LoginErrorCode.UNKNOWN_ACCOUNT, response_pkt.error)


if __name__ == '__main__':
    unittest.main()
