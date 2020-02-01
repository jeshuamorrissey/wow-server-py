load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "database",
    srcs = glob([
        "*.py",
    ]),
    visibility = ["//visibility:public"],
    deps = [
        ":common",
        requirement("pony"),
    ],
)

py_library(
    name = "common",
    srcs = ["common.py"],
    deps = [requirement("pony")],
)
