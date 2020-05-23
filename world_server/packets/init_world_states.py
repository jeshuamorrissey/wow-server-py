from construct import GreedyRange, Int16ul, Int32ul, Rebuild, Struct

ServerInitWorldStates = Struct(
    'map' / Int32ul,
    'zone' / Int32ul,
    'n_blocks' / Rebuild(Int16ul, lambda this: len(this.blocks)),
    'blocks' / GreedyRange(Struct(
        'state' / Int32ul,
        'value' / Int32ul,
    )),
)
