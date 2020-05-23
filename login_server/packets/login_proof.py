from construct import BytesInteger, Const, If, Int8ul, Struct

from login_server import op_code, router

ClientLoginProof = router.ClientPacket.Register(
    op_code.Client.LOGIN_PROOF,
    Struct(
        'A' / BytesInteger(32, swapped=True),
        'M' / BytesInteger(20, swapped=True),
        'crc_hash' / BytesInteger(20, swapped=True),
        'number_of_keys' / Int8ul,
        'security_flags' / Int8ul,
    ))

ServerLoginProof = Struct(
    'error' / Int8ul,
    'proof' / If(lambda self: self.error == 0,
                 Struct(
                     'proof' / BytesInteger(20, swapped=True),
                     'unk1' / Const(int(0).to_bytes(4, 'little')),
                 )),
)
