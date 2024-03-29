from typing import List, Tuple

from pony import orm

from common import srp
from database import enums, world
from login_server import op_code, router, session
from login_server.packets import login_challenge


@router.Handler(op_code.Client.LOGIN_CHALLENGE)
@orm.db_session
def handle_login_challenge(pkt: login_challenge.ClientLoginChallenge,
                           session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    account = world.Account.get(name=pkt.account_name)
    if not account:
        return [(
            op_code.Server.LOGIN_CHALLENGE,
            login_challenge.ServerLoginChallenge.build(dict(
                error=enums.LoginErrorCode.UNKNOWN_ACCOUNT,
                challenge=None,
            )),
        )]

    b, B = srp.GenerateEphemeral(account.verifier)

    session.account_name = account.name
    session.b = b
    session.B = B
    return [
        (
            op_code.Server.LOGIN_CHALLENGE,
            login_challenge.ServerLoginChallenge.build(
                dict(
                    error=enums.LoginErrorCode.OK,
                    challenge=dict(
                        B=B,
                        salt=account.salt,
                        crc_salt=srp.Random(16),
                    ),
                )),
        ),
    ]
