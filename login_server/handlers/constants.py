import enum


class LoginErrorCode(enum.IntEnum):
    OK = 0x00
    FAILED = 0x01  # "unable to connect"
    FAILED2 = 0x02  # "unable to connect"
    BANNED = 0x03  # "this account has been closed"
    UNKNOWN_ACCOUNT = 0x04  # "information is not valid"
    UNKNOWN_ACCOUNT3 = 0x05  # "information is not valid"
    ALREADYONLINE = 0x06  # "this account is already logged in"
    NOTIME = 0x07  # "you have no time left on this account"
    DBBUSY = 0x08  # "could not log in at this time, try again later"
    BADVERSION = 0x09  # "unable to validate game version"
    DOWNLOAD_FILE = 0x0A
    FAILED3 = 0x0B  # "unable to connect"
    SUSPENDED = 0x0C  # "this account has been temporarily suspended"
    FAILED4 = 0x0D  # "unable to connect"
    CONNECTED = 0x0E
    PARENTALCONTROL = 0x0F  # "blocked by parental controls"
    LOCKED_ENFORCED = 0x10  # "disconnected from server"
