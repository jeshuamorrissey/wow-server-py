from typing import Callable, Dict

from construct import Struct

from common import router
from login_server import op_code


class LoginClientPacket(router.Router):
    ROUTES: Dict[op_code.Client, Struct] = {}


class LoginHandler(router.Router):
    ROUTES: Dict[op_code.Client, Callable] = {}
