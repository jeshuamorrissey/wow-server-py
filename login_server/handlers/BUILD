load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "handlers",
    srcs = glob([
        "*.py",
    ]),
    visibility = ["//login_server:__subpackages__"],
    deps = [
        ":constants",
        "//database",
        "//login_server:op_code",
        requirement("construct"),
    ],
)

py_library(
    name = "constants",
    srcs = ["constants.py"],
)
