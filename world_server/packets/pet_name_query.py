from construct import CString, Int32ul, Int64ul, Struct

from world_server import op_code, router

ClientPetNameQuery = router.ClientPacket.Register(
    op_code.Client.PET_NAME_QUERY,
    Struct(
        'pet_number' / Int32ul,
        'pet_guid' / Int64ul,
    ),
)

ServerPetNameQuery = Struct(
    'number' / Int32ul,
    'name' / CString('ascii'),
    'name_timestamp' / Int32ul,
)
