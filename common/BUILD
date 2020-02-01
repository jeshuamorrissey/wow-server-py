load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "server",
    srcs = ["server.py"],
    deps = [
        requirement("coloredlogs"),
        requirement("construct"),
    ],
)

py_library(
    name = "router",
    srcs = ["router.py"],
)

py_library(
    name = "session",
    srcs = ["session.py"],
)

py_library(
    name = "srp",
    srcs = ["srp.py"],
)
