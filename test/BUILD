load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library", "py_test")

py_library(
    name = "test_lib",
    srcs = ["conftest.py"],
    data = [
        "base.db",
        "pytest.ini",
    ],
    deps = [
        "//common:server",
        "//database:common",
        "//database/constants",
        "//database/game",
        "//database/world",
        requirement("pony"),
        requirement("pytest-mock"),
        requirement("pytest"),
    ],
)

py_library(
    name = "login_server_test",
    deps = [
        ":test_lib",
        "//login_server:op_code",
        "//login_server:router",
        "//login_server:session",
        "//login_server/handlers",
        "//login_server/packets",
    ],
)

py_test(
    name = "test_login_server_login_challenge",
    srcs = ["test_login_server_login_challenge.py"],
    deps = [":login_server_test"],
)

py_test(
    name = "test_login_server_login_proof",
    srcs = ["test_login_server_login_proof.py"],
    deps = [":login_server_test"],
)

py_test(
    name = "test_login_server_realmlist",
    srcs = ["test_login_server_realmlist.py"],
    deps = [":login_server_test"],
)

py_library(
    name = "world_server_test",
    deps = [
        ":test_lib",
        "//world_server:op_code",
        "//world_server:router",
        "//world_server:session",
        "//world_server:system",
        "//world_server/handlers",
        "//world_server/packets",
    ],
)

py_test(
    name = "test_world_server_auth_session",
    srcs = ["test_world_server_auth_session.py"],
    deps = [":world_server_test"],
)
