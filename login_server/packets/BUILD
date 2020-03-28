load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "packets",
    srcs = glob(["*.py"]),
    visibility = ["//visibility:public"],
    deps = [
        "//common:srp",
        "//login_server:op_code",
        "//login_server:router",
        requirement("construct"),
    ],
)
