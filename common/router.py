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

    def __init__(self, key):
        self._key = key

    def __call__(self, fn: Callable):
        self.ROUTES[self._key] = fn
        return fn

    @classmethod
    def Register(cls, k, v):
        cls.ROUTES[k] = v
        return v
