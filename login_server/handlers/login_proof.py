from typing import Any, Dict, List, Text

from database import db
from login_server import op_code, router, session, srp
from login_server.handlers import constants as c
from login_server.packets import login_proof


@router.Handler(op_code.Client.LOGIN_PROOF)
def handle_login_proof(pkt: login_proof.ClientLoginProof,
                       state: session.State) -> List[bytes]:
    if not all((state.account, state.b, state.B)):
        return [
            login_proof.ServerLoginProof.build(
                dict(
                    error=c.LoginErrorCode.FAILED,
                    proof=None,
                ))
        ]

    account = state.account

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
        return [
            login_proof.ServerLoginProof.build(
                dict(
                    error=c.LoginErrorCode.UNKNOWN_ACCOUNT,
                    proof=None,
                ))
        ]

    # Authenticated! Save the session key...
    account.session_key = K
    db.commit()

    # ... and now send back proof we are a valid server.
    proof = srp.CalculateServerProof(
        A=pkt.A,
        M=M,
        K=K,
    )

    return [
        login_proof.ServerLoginProof.build(
            dict(
                error=c.LoginErrorCode.OK,
                proof=dict(proof=proof),
            ))
    ]
