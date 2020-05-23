from construct import (Bytes, BytesInteger, Compressed, CString, Default, Int32ul, Struct)

from world_server import op_code, router

ClientAuthSession = router.ClientPacket.Register(
    op_code.Client.AUTH_SESSION,
    Struct(
        'build_number' / Int32ul,
        'unk1' / Default(Int32ul, 0),
        'account_name' / CString('ascii'),
        'client_seed' / Int32ul,
        'client_proof' / BytesInteger(20, swapped=True),
        'addon_size' / Int32ul,
        'addons' / Compressed(
            Bytes(lambda this: this.addon_size),
            'zlib',
            level=6,
        ),
    ))
