import enum

import pytest

from common import router


class FakeOpCode(enum.IntEnum):
    OP1 = 1
    OP2 = 2


def test_router():
    router.Router.ROUTES = {}
    router.Router.Register(FakeOpCode.OP1, '1')

    router.Router(FakeOpCode.OP2)(test_router)

    assert len(router.Router.ROUTES) == FakeOpCode.OP2
    assert router.Router.ROUTES[FakeOpCode.OP1] == '1'
    assert router.Router.ROUTES[FakeOpCode.OP2] == test_router


def test_router_multiple_register_decorator():
    router.Router.ROUTES = {}

    router.Router(FakeOpCode.OP2)(test_router)

    with pytest.raises(RuntimeError):
        router.Router(FakeOpCode.OP2)(test_router_multiple_register_decorator)

    assert len(router.Router.ROUTES) == 1
    assert router.Router.ROUTES[FakeOpCode.OP2] == test_router


def test_router_multiple_register_fn():
    router.Router.ROUTES = {}

    router.Router.Register(FakeOpCode.OP2, '1')

    with pytest.raises(RuntimeError):
        router.Router.Register(FakeOpCode.OP2, '2')

    assert len(router.Router.ROUTES) == 1
    assert router.Router.ROUTES[FakeOpCode.OP2] == '1'
