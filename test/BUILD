load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "fake_db",
    srcs = ["fake_db.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//database:common",
        "//database/constants",
        "//database/game",
        "//database/world",
    ],
)
