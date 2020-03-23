load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library", "py_test")

py_library(
    name = "handlers",
    srcs = glob(["*.py"]),
    visibility = ["//login_server:__subpackages__"],
    deps = [
        ":constants",
        "//database/game",
        "//database/world",
        "//login_server:op_code",
        "//login_server:router",
        "//login_server:session",
        "//login_server/packets",
        "//world_server:system",
        requirement("pony"),
    ],
)

py_library(
    name = "constants",
    srcs = ["constants.py"],
)

py_test(
    name = "test_login_challenge",
    srcs = ["test_login_challenge.py"],
    deps = [
        ":handlers",
        "//common:server",
        "//test:fake_db",
    ],
)
