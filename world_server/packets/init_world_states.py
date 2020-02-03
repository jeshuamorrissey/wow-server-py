from construct import Int32ul, Float32l, Struct, Int16ul, Rebuild, GreedyRange

ServerInitWorldStates = Struct(
    'map' / Int32ul,
    'zone' / Int32ul,
    'n_blocks' / Rebuild(Int16ul, lambda this: len(this.blocks)),
    'blocks' / GreedyRange(Struct(
        'state' / Int32ul,
        'value' / Int32ul,
    )),
)
