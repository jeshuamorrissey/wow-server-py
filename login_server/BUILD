load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_binary(
    name = "login_server",
    srcs = ["main.py"],
    main = "main.py",
    deps = [
        ":session",
        "//login_server/packets:login_challenge",
    ],
)

py_library(
    name = "session",
    srcs = ["session.py"],
)
