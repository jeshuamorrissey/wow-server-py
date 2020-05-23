from construct import Int8ul, Int32ul, Struct

ServerMeetingstoneSetqueue = Struct(
    'area_id' / Int32ul,
    'status' / Int8ul,
)
