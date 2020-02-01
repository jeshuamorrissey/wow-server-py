from typing import Any, Dict, List, Text, Tuple

from pony import orm

from database.account import Account
from database.db import db
from login_server import op_code, router, session, srp
from login_server.handlers import constants as c
from login_server.packets import login_proof


@router.LoginHandler(op_code.Client.LOGIN_PROOF)
@orm.db_session
def handle_login_proof(
        pkt: login_proof.ClientLoginProof,
        state: session.State) -> List[Tuple[op_code.Server, bytes]]:
    if not all((state.account_name, state.b, state.B)):
        return [(
            op_code.Server.LOGIN_PROOF,
            login_proof.ServerLoginProof.build(
                dict(
                    error=c.LoginErrorCode.FAILED,
                    proof=None,
                )),
        )]

    account = Account[state.account_name]

    # Calculate our K and re-calculate M (to confirm client).
    K, M = srp.CalculateSessionKey(
        A=pkt.A,
        B=state.B,
        b=state.b,
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
