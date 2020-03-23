from construct import Int8ul, Struct

from world_server import op_code, router

ClientSwapInvItem = router.ClientPacket.Register(
    op_code.Client.SWAP_INV_ITEM,
    Struct(
        'src_slot' / Int8ul,
        'dst_slot' / Int8ul,
    ),
)
