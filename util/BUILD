load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "dbc_loader",
    srcs = ["dbc_loader.py"],
    deps = [
        requirement("mpyq"),
        requirement("construct"),
        "//database:common",
        "//database/dbc",
    ],
)

py_binary(
    name = "gen_enums",
    srcs = ["gen_enums.py"],
    deps = [
        "//database:common",
        "//database/dbc",
        "//database/world",
        requirement("stringcase"),
    ],
)
