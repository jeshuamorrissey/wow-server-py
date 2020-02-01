import enum

from construct import Const, If, Int8ul, Struct

from world_server import op_code, router


class ErrorCode(enum.IntEnum):
    OK = 0x0C
    FAILED = 0x0D
    REJECT = 0x0E
    BAD_SERVER_PROOF = 0x0F
    UNAVAILABLE = 0x10
    SYSTEM_ERROR = 0x11
    BILLING_ERROR = 0x12
    BILLING_EXPIRED = 0x13
    VERSION_MISMATCH = 0x14
    UNKNOWN_ACCOUNT = 0x15
    INCORRECT_PASSWORD = 0x16
    SESSION_EXPIRED = 0x17
    SERVER_SHUTTING_DOWN = 0x18
    ALREADY_LOGGING_IN = 0x19
    LOGIN_SERVER_NOT_FOUND = 0x1A
    WAIT_QUEUE = 0x1B
    BANNED = 0x1C
    ALREADY_ONLINE = 0x1D
    NO_TIME = 0x1E
    DB_BUSY = 0x1F
    SUSPENDED = 0x20
    PARENTAL_CONTROL = 0x21


ServerAuthResponse = Struct(
    'error' / Int8ul,
    'billing' / If(
        lambda self: self.error == ErrorCode.OK,
        Struct(
            'time_remaining' / Const(b'\x00\x00\x00\x00'),
            'flags' / Const(b'\x00'),
            'time_requested' / Const(b'\x00\x00\x00\x00'),
        )),
)
