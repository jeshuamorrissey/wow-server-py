"""Rules for generating files using the kaitai-struct-compiler."""

load("@rules_python//python:defs.bzl", "py_library")
load("@requirements//:requirements.bzl", "requirement")

def kaitai_packet(ksy, kaitai_compile_cmd = "kaitai-struct-compiler"):
    """Bazel rule which will generate the Python file from the given key file.

    Args:
        ksy: str, the .ksy file to compile.
        kaitai_compile_cmd: str, the command to use to compiler the struct.
    """
    name = ksy.replace(".ksy", "")
    genrule_name = name + ".genrule"
    output = name + ".py"
    native.genrule(
        name = genrule_name,
        srcs = [ksy],
        outs = [output],
        cmd = "%s $(location %s) --target python --outdir $$(dirname $(location %s))" % (kaitai_compile_cmd, ksy, output),
    )

    py_library(
        name = name,
        srcs = [":" + genrule_name],
        deps = [
            requirement("kaitaistruct"),
        ],
    )
