from construct import Int32ul, Float32l, Struct

ServerLoginVerifyWorld = Struct(
    'map' / Int32ul,
    'x' / Float32l,
    'y' / Float32l,
    'z' / Float32l,
    'o' / Float32l,
)
