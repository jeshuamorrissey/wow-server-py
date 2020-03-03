from construct import Int8ul, Int32ul, Struct

ServerUpdateAuraDuration = Struct(
    'slot' / Int8ul,
    'duration' / Int32ul,
)
