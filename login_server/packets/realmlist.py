from construct import (BitStruct, Const, CString, Flag, Float32l, GreedyRange, Int8ul, Int32ul, Padding, Rebuild,
                       Struct)

from login_server import op_code, router

ClientRealmlist = router.ClientPacket.Register(op_code.Client.REALMLIST,
                                               Struct('unk1' / Const(int(0).to_bytes(4, 'little'))))

ServerRealmlist = Struct(
    'unk1' / Const(int(0).to_bytes(4, 'little')),
    'n_realms' / Rebuild(Int8ul, lambda this: len(this.realms)),
    'realms' / GreedyRange(
        Struct(
            'icon' / Int32ul,
            'flags' / BitStruct(
                'is_full' / Flag,  # "full" population
                'is_recommended' / Flag,  # recommended in green text
                'for_new_players' / Flag,  # recommended in blue text
                'unused' / Padding(3),
                'is_offline' / Flag,  # marks as offline
                'is_unavailable' / Flag,  # shows name in red
            ),
            'name' / CString('ascii'),
            'hostport' / CString('ascii'),
            'population' / Float32l,  # relative population of realms
            'n_characters' / Int8ul,
            'zone' / Const(b'\x01'),  # Will show as "English"
            'unk' / Const(b'\x00'),
        )),
    'unk2' / Const(int(2).to_bytes(2, 'little')),
)
