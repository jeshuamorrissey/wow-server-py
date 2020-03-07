load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "dbc_loader",
    srcs = ["dbc_loader.py"],
    deps = [
        requirement("mpyq"),
        requirement("construct"),
    ],
)
