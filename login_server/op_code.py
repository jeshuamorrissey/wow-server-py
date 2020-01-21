import enum

from construct import Int8ul

OpCode = Int8ul


class Server(enum.IntEnum):
    LOGIN_CHALLENGE = 0x00
    LOGIN_PROOF = 0x01
    RECONNECT_CHALLENGE = 0x02
    RECONNECT_PROOF = 0x03
    REALMLIST = 0x10
    TRANSFER_INITIATE = 0x30
    TRANSFER_DATA = 0x31


class Client(enum.IntEnum):
    LOGIN_CHALLENGE = 0x00
    LOGIN_PROOF = 0x01
    RECONNECT_CHALLENGE = 0x02
    RECONNECT_PROOF = 0x03
    REALMLIST = 0x10
    TRANSFER_INITIATE = 0x30
    TRANSFER_DATA = 0x31
