load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "world_server",
    visibility = ["//visibility:public"],
    deps = [
        ":op_code",
        ":router",
        ":session",
        ":system",
        "//world_server/handlers",
        "//world_server/packets",
        "//world_server/systems",
    ],
)

py_library(
    name = "session",
    srcs = ["session.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":op_code",
        "//common:session",
        "//common:srp",
        "//world_server/packets",
    ],
)

py_library(
    name = "op_code",
    srcs = ["op_code.py"],
    visibility = ["//visibility:public"],
)

py_library(
    name = "router",
    srcs = ["router.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":op_code",
        "//common:router",
        requirement("construct"),
    ],
)

py_library(
    name = "system",
    srcs = ["system.py"],
    visibility = ["//visibility:public"],
)

py_library(
    name = "config",
    srcs = ["config.py"],
    visibility = ["//visibility:public"],
)
