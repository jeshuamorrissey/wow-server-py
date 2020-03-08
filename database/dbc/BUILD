load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "dbc",
    srcs = glob([
        "**/*.py",
    ]),
    data = glob(["data/*"]),
    visibility = ["//visibility:public"],
    deps = [
        requirement("pony"),
        "//database:db",
    ],
)
