load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "database",
    visibility = ["//visibility:public"],
    deps = [
        ":db",
        "//database/constants",
        "//database/game",
        "//database/world",
    ],
)

py_library(
    name = "db",
    srcs = [
        "data.py",
        "db.py",
    ],
    visibility = ["//visibility:public"],
    deps = [
        requirement("pony"),
        ":common",
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
