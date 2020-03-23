load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "login_server",
    visibility = ["//visibility:public"],
    deps = [
        ":op_code",
        ":router",
        ":session",
        "//login_server/handlers",
        "//login_server/packets",
    ],
)

py_library(
    name = "session",
    srcs = ["session.py"],
    visibility = ["//login_server:__subpackages__"],
    deps = [
        ":op_code",
        "//common:session",
    ],
)

py_library(
    name = "op_code",
    srcs = ["op_code.py"],
    visibility = ["//login_server:__subpackages__"],
)

py_library(
    name = "router",
    srcs = ["router.py"],
    visibility = ["//login_server:__subpackages__"],
    deps = [
        ":op_code",
        "//common:router",
        requirement("construct"),
    ],
)
