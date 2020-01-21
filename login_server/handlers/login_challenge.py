from typing import Dict, List

from login_server import db, op_code, router, srp
from login_server.packets import login_challenge


@router.Handler(op_code.Client.LOGIN_CHALLENGE)
def handle_login_challenge(pkt: login_challenge.ClientLoginChallenge,
                           state: Dict) -> List[bytes]:
    account = db.db.get(f'account::{pkt.account_name.lower()}', None)
    if not account:
        return []

    b, B = srp.GenerateEphemeral(account['verifier'])

    state['account'] = account
    state['b'] = b
    print(account)
    return [
        login_challenge.ServerLoginChallenge.build(
            dict(
                error=0,
                challenge=dict(
                    B=B,
                    salt=account['salt'],
                    crc_salt=0,
                ),
            ))
    ]
