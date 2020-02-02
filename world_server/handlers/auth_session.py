from typing import List, Tuple

from pony import orm

from common import srp
from database.world.account import Account
from world_server import op_code, router, session
from world_server.packets import auth_response, auth_session


@router.Handler(op_code.Client.AUTH_SESSION)
@orm.db_session
def handle_auth_session(
        pkt: auth_session.ClientAuthSession,
        session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    # Retreive account from database and save session key.
    account = Account[pkt.account_name]
    if not account:
        return [(
            op_code.Server.AUTH_RESPONSE,
            auth_response.ServerAuthResponse.build(
                dict(error=auth_response.ErrorCode.UNKNOWN_ACCOUNT)),
        )]

    # Save details about the account.
    session.account_name = account.name
    session.session_key = account.session_key
    session.session_key_b = session.session_key.to_bytes(40, 'little')

    # Validate the client proof.
    proof = srp.CalculateAuthSessionProof(
        pkt.account_name,
        b'\x00\x00\x00\x00',  # something time related, always 0
        pkt.client_seed.to_bytes(4, 'little'),
        session.auth_challenge_seed.to_bytes(4, 'big'),
        session.session_key_b,
    )

    if proof != pkt.client_proof:
        return [(
            op_code.Server.AUTH_RESPONSE,
            auth_response.ServerAuthResponse.build(
                dict(error=auth_response.ErrorCode.FAILED)),
        )]

    return [(
        op_code.Server.AUTH_RESPONSE,
        auth_response.ServerAuthResponse.build(
            dict(error=auth_response.ErrorCode.OK)),
    )]
