from typing import Any, Dict, List, Text, Tuple

from pony import orm

from database.account import Account
from login_server import op_code, router, session, srp
from login_server.handlers import constants as c
from login_server.packets import login_challenge


@router.LoginHandler(op_code.Client.LOGIN_CHALLENGE)
@orm.db_session
def handle_login_challenge(
        pkt: login_challenge.ClientLoginChallenge,
        state: session.State) -> List[Tuple[op_code.Server, bytes]]:
    account = Account[pkt.account_name]
    if not account:
        return [(
            op_code.Server.LOGIN_CHALLENGE,
            login_challenge.ServerLoginChallenge.build(
                dict(
                    error=c.LoginErrorCode.UNKNOWN_ACCOUNT,
                    challenge=None,
                )),
        )]

    b, B = srp.GenerateEphemeral(account.verifier)

    state.account_name = account.name
    state.b = b
    state.B = B
    return [
        (
            op_code.Server.LOGIN_CHALLENGE,
            login_challenge.ServerLoginChallenge.build(
                dict(
                    error=c.LoginErrorCode.OK,
                    challenge=dict(
                        B=B,
                        salt=account.salt,
                        crc_salt=srp.Random(16),
                    ),
                )),
        ),
    ]
