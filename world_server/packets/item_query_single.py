from construct import Int32ul, Int64ul, Struct, Int32sl, CString, Float32l, Array

from world_server import op_code, router

ClientItemQuerySingle = router.ClientPacket.Register(
    op_code.Client.ITEM_QUERY_SINGLE,
    Struct(
        'entry' / Int32ul,
        'guid' / Int64ul,
    ),
)

ServerItemQuerySingle = Struct(
    'entry' / Int32ul,
    'class_' / Int32ul,
    'subclass' / Int32ul,
    'name' / CString('ascii'),
    'name_2' / CString('ascii'),
    'name_3' / CString('ascii'),
    'name_4' / CString('ascii'),
    'display_info_id' / Int32ul,
    'quality' / Int32ul,
    'flags' / Int32ul,
    'buy_price' / Int32ul,
    'sell_price' / Int32ul,
    'inventory_type' / Int32ul,
    'allowable_class' / Int32sl,
    'allowable_race' / Int32sl,
    'item_level' / Int32ul,
    'required_level' / Int32ul,
    'required_skill' / Int32ul,
    'required_skill_rank' / Int32ul,
    'required_spell' / Int32ul,
    'required_honor_rank' / Int32ul,
    'required_city_rank' / Int32ul,
    'required_reputation_faction' / Int32ul,
    'required_reputation_faction_2' / Int32ul,
    'max_count' / Int32ul,
    'stackable' / Int32ul,
    'container_slots' / Int32ul,
    'stats' / Array(
        10,
        Struct(
            'type' / Int32ul,
            'value' / Int32sl,
        ),
    ),
    'damages' / Array(
        5,
        Struct(
            'min' / Float32l,
            'max' / Float32l,
            'type' / Int32ul,
        ),
    ),
    'armor' / Int32ul,
    'holy_res' / Int32ul,
    'fire_res' / Int32ul,
    'nature_res' / Int32ul,
    'frost_res' / Int32ul,
    'shadow_res' / Int32ul,
    'arcane_res' / Int32ul,
    'delay' / Int32ul,
    'ammo_type' / Int32ul,
    'ranged_mod_range' / Float32l,
    'spells' / Array(
        5,
        Struct(
            'id' / Int32ul,
            'trigger' / Int32ul,
            'charges' / Int32sl,
            'cooldown' / Int32sl,
            'category' / Int32ul,
            'category_cooldown' / Int32sl,
        ),
    ),
    'bonding' / Int32ul,
    'description' / CString('ascii'),
    'page_text' / Int32ul,
    'language_id' / Int32ul,
    'page_material' / Int32ul,
    'start_quest' / Int32ul,
    'lock_id' / Int32ul,
    'material' / Int32ul,
    'sheath' / Int32ul,
    'random_property' / Int32ul,
    'block' / Int32ul,
    'item_set' / Int32ul,
    'max_durability' / Int32ul,
    'area' / Int32ul,
    'map' / Int32ul,
    'bag_family' / Int32ul,
)
