load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_binary(
    name = "login_server",
    srcs = ["main.py"],
    main = "main.py",
    deps = [
        ":db",
        ":router",
        ":session",
        ":srp",
        "//login_server/handlers",
        "//login_server/packets",
    ],
)

py_library(
    name = "session",
    srcs = ["session.py"],
    deps = [
        ":op_code",
    ],
)

py_library(
    name = "op_code",
    srcs = ["op_code.py"],
    visibility = ["//login_server:__subpackages__"],
    deps = [
        requirement("construct"),
    ],
)

py_library(
    name = "router",
    srcs = ["router.py"],
    visibility = ["//login_server:__subpackages__"],
    deps = [
        ":op_code",
        requirement("construct"),
    ],
)

py_library(
    name = "db",
    srcs = ["db.py"],
    visibility = ["//login_server:__subpackages__"],
    deps = [
        requirement("sqlitedict"),
    ],
)

py_library(
    name = "srp",
    srcs = ["srp.py"],
    visibility = ["//login_server:__subpackages__"],
    deps = [
    ],
)
