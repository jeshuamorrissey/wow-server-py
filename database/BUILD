load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "database",
    srcs = [
        "__init__.py",
    ],
    visibility = ["//visibility:public"],
    deps = [":account"],
)

py_library(
    name = "account",
    srcs = ["account.py"],
)
