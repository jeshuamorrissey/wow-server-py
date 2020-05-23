from construct import Struct

from world_server import op_code, router

ClientRequestPetInfo = router.ClientPacket.Register(
    op_code.Client.REQUEST_PET_INFO,
    Struct(),
)
