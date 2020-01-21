from typing import Callable, Dict, Optional

from construct import Struct

from login_server import op_code


class ClientPacket(object):
    _PACKETS: Dict[op_code.Client, Struct] = {}

    @classmethod
    def Register(cls, op_code: op_code.Client, format: Struct) -> Struct:
        """Register a new packet for a given opcode.

        Args:
            op_code: The opcode corresponding to this packet.
            format: The format of the opcode.

        Returns:
            The same struct format passed as input.
        """
        cls._PACKETS[op_code] = format
        return format

    @classmethod
    def Get(cls, op_code: op_code.Client) -> Optional[Struct]:
        """Get the packet corresponding to an opcode.

        Args:
            op_code: The opcode corresponding to the packet.
        
        Returns:
            The format of the packet, or None if it is unregistered.
        """
        return cls._PACKETS.get(op_code, None)


class Handler(object):
    """Decorator which can be used to register a function as an opcode handler."""

    _HANDLERS: Dict[op_code.Client, Callable] = {}

    def __init__(self, op_code: op_code.Client):
        self._op_code = op_code

    def __call__(self, f: Callable):
        self._HANDLERS[self._op_code] = f
        return f

    @classmethod
    def Get(cls, op_code: op_code.Client) -> Optional[Callable]:
        """Get the opcode handler for a given code.

        Args:
            op_code: The opcode to get the handler of.
        
        Returns:
            The function which can be used to handle the opcode.
        """
        return cls._HANDLERS.get(op_code, None)
