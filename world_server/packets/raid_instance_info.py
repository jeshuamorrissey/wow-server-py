from construct import Array, Int32ul, Rebuild, Struct

ServerRaidInstanceInfo = Struct(
    'count' / Rebuild(Int32ul, lambda c: len(c.instances)),
    'instances' / Array(lambda c: c.count, Struct(
        'map_id' / Int32ul,
        'reset_time' / Int32ul,
        'instance_id' / Int32ul,
    )),
)
