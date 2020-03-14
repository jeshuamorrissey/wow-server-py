load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "dbc_loader",
    srcs = ["dbc_loader.py"],
    deps = [
        "//database/constants",
        requirement("coloredlogs"),
        requirement("construct"),
        requirement("mpyq"),
    ],
)

py_binary(
    name = "make_world_handler",
    srcs = ["make_world_handler.py"],
    deps = [
        "//world_server:op_code",
    ],
)

py_binary(
    name = "gen_enums",
    srcs = ["gen_enums.py"],
    deps = [
        "//database",
        requirement("coloredlogs"),
        requirement("stringcase"),
    ],
)
