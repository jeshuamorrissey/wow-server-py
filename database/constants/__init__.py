"""A module for all unchangeable database values.

These are database values pull from the client data files, so cannot
be changed. They are typically only lookup tables (or similar), but
also include all of the spells.

The data directory can be re-generated using the dbc_loader util (run from the base directory):

    $ bazel run //util:dbc_loader -- --wow_dir "${WOW_DIR?}" --output_dir "$(pwd)/database/dbc/data"

The data files contain gzipped JSON files which can be loaded using `LoadDBC()`.

Based on this data, enum values can be auto-generated using gen_enums.py:

    $ bazel run //util:gen_enums -- --output_file "$(pwd)/database/constants/enums.py"

TODO(jeshua): make a framework for changing these. This would required
              building a new patch MPQ for the client.
"""
