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
from .animation_data import *
from .area_poi import *
from .area_trigger import *
from .attack_anim_kits import *
from .attack_anim_types import *
from .auction_house import *
from .bank_bag_slot_prices import *
from .chr_classes import *
from .chr_races import *
from .cinematic_camera import *
from .cinematic_sequences import *
from .creature_type import *
from .enum import *
from .faction import *
from .item_class import *
from .languages import *
from .resistances import *
from .spell import *
