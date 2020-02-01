from construct import (BytesInteger, Const, If, Int8ul, Int16ul, Int32ub,
                       Int32ul, PaddedString, PascalString, Struct)

from login_server import op_code, router, srp

ClientLoginChallenge = router.LoginClientPacket.Register(
    op_code.Client.LOGIN_CHALLENGE,
    Struct(
        'game_name' / PaddedString(4, 'ascii'),
        'version_major' / Int8ul,
        'version_minor' / Int8ul,
        'version_bug' / Int8ul,
        'build' / Int16ul,
        'platform' / PaddedString(4, 'ascii'),
        'os' / PaddedString(4, 'ascii'),
        'locale' / PaddedString(4, 'ascii'),
        'timezone_offset' / Int32ul,
        'ip_address' / Int32ub,
        'account_name' / PascalString(Int8ul, 'ascii'),
    ))

ServerLoginChallenge = Struct(
    'unk1' / Const(b'\x00'),
    'error' / Int8ul,
    'challenge' / If(
        lambda self: self.error == 0,
        Struct(
            'B' / BytesInteger(32, swapped=True),
            'g_len' / Const(b'\x01'),
            'g' / Const(int(srp.g).to_bytes(1, 'little')),
            'N_len' / Const(int(32).to_bytes(1, 'little')),
            'N' / Const(int(srp.N).to_bytes(32, 'little')),
            'salt' / BytesInteger(32, swapped=True),
            'crc_salt' / BytesInteger(16, swapped=True),
            'unk2' / Const(b'\x00'),
        )),
)
