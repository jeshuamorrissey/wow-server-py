load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "systems",
    srcs = glob([
        "*.py",
    ]),
    visibility = ["//visibility:public"],
    deps = [
        "//database",
        "//world_server:system",
    ],
)
