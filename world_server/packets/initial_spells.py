from construct import Array, Const, Int16ul, Int32ul, Rebuild, Struct

ServerInitialSpells = Struct(
    Const(b'\x00'),
    'spell_count' / Rebuild(Int16ul, lambda c: len(c.spells)),
    'spells' /
    Array(lambda c: c.spell_count, Struct(
        'id' / Int16ul,
        Const(b'\x00\x00'),
    )),
    'spell_cooldown_count' /
    Rebuild(Int16ul, lambda c: len(c.spell_cooldowns)),
    'spell_cooldowns' / Array(
        lambda c: c.spell_cooldown_count,
        Struct(
            'id' / Int16ul,
            'cast_item_id' / Int16ul,
            'category' / Int16ul,
            'cooldown' / Int32ul,
            'category_cooldown' / Int32ul,
        )),
)
