from construct import GreedyBytes, Struct

from world_server import op_code, router

ClientUpdateAccountData = router.ClientPacket.Register(
    op_code.Client.UPDATE_ACCOUNT_DATA,
    Struct('data' / GreedyBytes),
)
