load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "packets",
    srcs = glob(["*.py"]),
    visibility = ["//world_server:__subpackages__"],
    deps = [
        "//world_server:op_code",
        "//world_server:router",
        requirement("construct"),
    ],
)
