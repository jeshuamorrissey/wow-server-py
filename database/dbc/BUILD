load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "dbc",
    srcs = glob([
        "**/*.py",
    ]),
    data = ["item_template.json.gz"],
    visibility = ["//visibility:public"],
    deps = [
        requirement("pony"),
    ],
)
