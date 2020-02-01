load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "database",
    srcs = [
        "account.py",
        "db.py",
        "realm.py",
    ],
    visibility = ["//visibility:public"],
    deps = [
        ":common",
        "//common:srp",
        requirement("pony"),
    ],
)

py_library(
    name = "common",
    srcs = ["common.py"],
    deps = [requirement("pony")],
)
