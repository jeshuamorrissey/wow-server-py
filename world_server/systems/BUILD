load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "systems",
    srcs = glob([
        "*.py",
    ]),
    visibility = ["//world_server:__subpackages__"],
    deps = [
        "//world_server:system",
    ],
)
