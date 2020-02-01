from typing import Callable, Dict

import construct

from common import router
from login_server import op_code


class ClientPacket(router.Router):
    ROUTES: Dict[op_code.Client, construct.Struct] = {}


class Handler(router.Router):
    ROUTES: Dict[op_code.Client, Callable] = {}
