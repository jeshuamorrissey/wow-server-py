from construct import Enum, Int8ul, Int32ul, Struct

from database import enums

ServerMeetingstoneSetqueue = Struct(
    'area_id' / Int32ul,
    'status' / Int8ul,
)
