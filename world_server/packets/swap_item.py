from construct import Int8ul, Struct

from world_server import op_code, router

ClientSwapItem = router.ClientPacket.Register(
    op_code.Client.SWAP_ITEM,
    Struct(
        'dest_bag' / Int8ul,
        'dest_slot' / Int8ul,
        'source_bag' / Int8ul,
        'source_slot' / Int8ul,
    ),
)
