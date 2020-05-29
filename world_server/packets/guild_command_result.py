from construct import CString, Enum, Int32ul, Struct

ServerGuildCommandResult = Struct(
    'cmd' / Int32ul,
    'str' / CString('ascii'),
    'result' / Int32ul,
)
