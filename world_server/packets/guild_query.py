from construct import Array, CString, Int32ul, Int64ul, Struct

from world_server import op_code, router

ClientGuildQuery = router.ClientPacket.Register(
    op_code.Client.GUILD_QUERY,
    Struct('id' / Int32ul),
)

ServerGuildQuery = Struct(
    'id' / Int32ul,
    'name' / CString('ascii'),
    'rank_names' / Array(10, CString('ascii')),
    'emblem_style' / Int32ul,
    'emblem_color' / Int32ul,
    'border_style' / Int32ul,
    'border_color' / Int32ul,
    'background_color' / Int32ul,
)
