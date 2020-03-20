from construct import Int32ul, Struct

from world_server import op_code, router

ClientTutorialFlag = router.ClientPacket.Register(
    op_code.Client.TUTORIAL_FLAG,
    Struct('flag' / Int32ul,),
)
