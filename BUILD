load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "wow_server",
    srcs = ["wow_server.py"],
    deps = [
        "//common:server",
        "//login_server",
    ],
)
