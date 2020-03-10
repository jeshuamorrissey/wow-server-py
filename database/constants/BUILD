load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "constants",
    srcs = glob(
        ["**/*.py"],
        exclude = ["common.py"],
    ),
    data = glob(["data/*"]),
    visibility = ["//visibility:public"],
    deps = [
        requirement("pony"),
        ":common",
        "//database:db",
        "//database/enums",
    ],
)

py_library(
    name = "common",
    srcs = ["common.py"],
)
