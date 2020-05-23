load("@requirements//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library", "py_test")

py_library(
    name = "test_lib",
    srcs = ["conftest.py"],
    data = [
        "base.db",
        "pytest.ini",
    ],
    deps = [
        "//common:server",
        "//database:common",
        "//database/constants",
        "//database/game",
        "//database/world",
        requirement("pony"),
        requirement("pytest-mock"),
        requirement("pytest"),

        # Bazel isn't auto-discovering requirements for some reason...
        requirement("six"),
        requirement("atomicwrites"),
        requirement("py"),
        requirement("pluggy"),
        requirement("importlib_metadata"),
        requirement("zipp"),
        requirement("packaging"),
        requirement("more_itertools"),
    ],
)

py_library(
    name = "login_server_test",
    deps = [
        ":test_lib",
        "//login_server:op_code",
        "//login_server:router",
        "//login_server:session",
        "//login_server/handlers",
        "//login_server/packets",
    ],
)

py_test(
    name = "test_login_server_login_challenge",
    srcs = ["test_login_server_login_challenge.py"],
    deps = [":login_server_test"],
)

py_test(
    name = "test_login_server_login_proof",
    srcs = ["test_login_server_login_proof.py"],
    deps = [":login_server_test"],
)

py_test(
    name = "test_login_server_realmlist",
    srcs = ["test_login_server_realmlist.py"],
    deps = [":login_server_test"],
)

py_library(
    name = "world_server_test",
    deps = [
        ":test_lib",
        "//world_server:op_code",
        "//world_server:router",
        "//world_server:session",
        "//world_server:system",
        "//world_server/handlers",
        "//world_server/packets",
        "//world_server/systems",
    ],
)

py_test(
    name = "test_world_server_auth_session",
    srcs = ["test_world_server_auth_session.py"],
    deps = [":world_server_test"],
)

py_test(
    name = "test_world_server_auto_equip_item",
    srcs = ["test_world_server_auto_equip_item.py"],
    deps = [":world_server_test"],
)

py_test(
    name = "test_world_server_char_create",
    srcs = ["test_world_server_char_create.py"],
    deps = [":world_server_test"],
)

py_test(
    name = "test_world_server_char_delete",
    srcs = ["test_world_server_char_delete.py"],
    deps = [":world_server_test"],
)

py_test(
    name = "test_world_server_char_enum",
    srcs = ["test_world_server_char_enum.py"],
    deps = [":world_server_test"],
)

py_test(
    name = "test_world_server_battlefield_status",
    srcs = ["test_world_server_battlefield_status.py"],
    deps = [":world_server_test"],
)

py_test(
    name = "test_world_server_gm_get_ticket",
    srcs = ["test_world_server_gm_get_ticket.py"],
    deps = [":world_server_test"],
)

py_test(
    name = "test_world_server_guild_query",
    srcs = ["test_world_server_guild_query.py"],
    deps = [":world_server_test"],
)

py_test(
    name = "test_world_server_item_query_single",
    srcs = ["test_world_server_item_query_single.py"],
    deps = [":world_server_test"],
)

py_test(
    name = "test_world_server_move_time_skipped",
    srcs = ["test_world_server_move_time_skipped.py"],
    deps = [":world_server_test"],
)

py_test(
    name = "test_world_server_ping",
    srcs = ["test_world_server_ping.py"],
    deps = [":world_server_test"],
)

py_test(
    name = "test_world_server_meetingstone_info",
    srcs = ["test_world_server_meetingstone_info.py"],
    deps = [":world_server_test"],
)

py_test(
    name = "test_world_server_name_query",
    srcs = ["test_world_server_name_query.py"],
    deps = [":world_server_test"],
)

py_test(
    name = "test_world_server_pet_name_query",
    srcs = ["test_world_server_pet_name_query.py"],
    deps = [":world_server_test"],
)
