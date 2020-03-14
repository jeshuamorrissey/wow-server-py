from construct import CString, Enum, Int32ul, Struct

from database import enums

ServerGuildCommandResult = Struct(
    'cmd' / Enum(Int32ul, enums.GuildCommandType),
    'str' / CString('ascii'),
    'result' / Enum(Int32ul, enums.GuildCommandError),
)
