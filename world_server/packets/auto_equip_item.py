from construct import Int8ul, Struct

from world_server import op_code, router

ClientAutoEquipItem = router.ClientPacket.Register(
    op_code.Client.AUTO_EQUIP_ITEM,
    Struct(
        'container_slot' / Int8ul,
        'item_slot' / Int8ul,
    ),
)
