load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "handlers",
    srcs = glob([
        "*.py",
    ]),
    visibility = ["//world_server:__subpackages__"],
    deps = [
        "//database",
    ],
)
