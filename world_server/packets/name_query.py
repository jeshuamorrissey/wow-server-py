from construct import CString, Int32ul, Int64ul, Struct

from world_server import op_code, router

ClientNameQuery = router.ClientPacket.Register(
    op_code.Client.NAME_QUERY,
    Struct('guid' / Int64ul),
)

ServerNameQuery = Struct(
    'guid' / Int64ul,
    'name' / CString('ascii'),
    'realm_name' / CString('ascii'),
    'race' / Int32ul,
    'gender' / Int32ul,
    'class_' / Int32ul,
)
