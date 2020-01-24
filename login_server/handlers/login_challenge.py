from typing import Any, Dict, List, Text

from database import db
from database.account import Account
from login_server import op_code, router, session, srp
from login_server.handlers import constants as c
from login_server.packets import login_challenge


@router.Handler(op_code.Client.LOGIN_CHALLENGE)
def handle_login_challenge(pkt: login_challenge.ClientLoginChallenge,
                           state: session.State) -> List[bytes]:
    account: Account = db.get(Account.Key(pkt.account_name), None)
    if not account:
        return [
            login_challenge.ServerLoginChallenge.build(
                dict(
                    error=c.LoginErrorCode.UNKNOWN_ACCOUNT,
                    challenge=None,
                ))
        ]

    b, B = srp.GenerateEphemeral(account.verifier)

    state.account = account
    state.b = b
    state.B = B
    return [
        login_challenge.ServerLoginChallenge.build(
            dict(
                error=c.LoginErrorCode.OK,
                challenge=dict(
                    B=B,
                    salt=account.salt,
                    crc_salt=0,
                ),
            ))
    ]
