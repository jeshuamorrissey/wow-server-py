load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "world",
    srcs = glob([
        "**/*.py",
    ]),
    visibility = ["//visibility:public"],
    deps = [
        "//common:srp",
        "//database:common",
        "//database:db",
        "//database/dbc",
        requirement("pony"),
    ],
)
