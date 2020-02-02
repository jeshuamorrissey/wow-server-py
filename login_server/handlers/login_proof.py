from typing import List, Tuple

from pony import orm

from common import srp
from database.world.account import Account
from login_server import op_code, router, session
from login_server.handlers import constants as c
from login_server.packets import login_proof


@router.Handler(op_code.Client.LOGIN_PROOF)
@orm.db_session
def handle_login_proof(
        pkt: login_proof.ClientLoginProof,
        session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    if not all((session.account_name, session.b, session.B)):
        return [(
            op_code.Server.LOGIN_PROOF,
            login_proof.ServerLoginProof.build(
                dict(
                    error=c.LoginErrorCode.FAILED,
                    proof=None,
                )),
        )]

    account = Account[session.account_name]

    # Calculate our K and re-calculate M (to confirm client).
    K, M = srp.CalculateSessionKey(
        A=pkt.A,
        B=session.B,
        b=session.b,
        v=account.verifier,
        s=account.salt,
        account_name=account.name,
    )

    if M != pkt.M:
        return [(
            op_code.Server.LOGIN_PROOF,
            login_proof.ServerLoginProof.build(
                dict(
                    error=c.LoginErrorCode.UNKNOWN_ACCOUNT,
                    proof=None,
                )),
        )]

    # Authenticated! Save the session key...
    account.session_key_str = str(K)

    # ... and now send back proof we are a valid server.
    proof = srp.CalculateServerProof(
        A=pkt.A,
        M=M,
        K=K,
    )

    return [
        (
            op_code.Server.LOGIN_PROOF,
            login_proof.ServerLoginProof.build(
                dict(
                    error=c.LoginErrorCode.OK,
                    proof=dict(proof=proof),
                )),
        ),
    ]
