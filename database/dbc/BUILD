load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "dbc",
    srcs = glob([
        "**/*.py",
    ]),
    visibility = ["//visibility:public"],
    deps = [
        requirement("pony"),
    ],
)
