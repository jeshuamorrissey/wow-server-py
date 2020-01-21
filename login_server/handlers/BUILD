load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "handlers",
    srcs = ["__init__.py"],
    visibility = ["//login_server:__subpackages__"],
    deps = [
        ":login_challenge",
    ],
)

py_library(
    name = "login_challenge",
    srcs = ["login_challenge.py"],
    deps = [
        "//login_server:db",
        "//login_server:op_code",
        requirement("construct"),
    ],
)
