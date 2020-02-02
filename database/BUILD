load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "db",
    srcs = [
        "db.py",
    ],
    visibility = ["//visibility:public"],
    deps = [
        requirement("pony"),
    ],
)

py_library(
    name = "common",
    srcs = [
        "common.py",
    ],
    visibility = ["//visibility:public"],
    deps = [
        requirement("pony"),
    ],
)
