import enum
from typing import Any, Callable, Dict, Optional


class Router(object):
    """Class which acts as a decorator or general registrar.
    
    Can be used as a decorator:
    
        @Router(key)
        def key_handler(...):
            ...
        
    ... or to register other things:
    
        Router.Register(key, ...)
    """
    ROUTES: Dict[Any, Any] = {}

    def __init__(self, key: enum.IntEnum):
        self._key = key

    def __call__(self, fn: Callable):
        if self._key in self.ROUTES:
            raise RuntimeError(f'Tried to register 2 handlers for op {self._key.name}')
        self.ROUTES[self._key] = fn
        return fn

    @classmethod
    def Register(cls, k: enum.IntEnum, v: Any):
        if k in cls.ROUTES:
            raise RuntimeError(f'Tried to register 2 packets for op {k.name}')
        cls.ROUTES[k] = v
        return v
