"""A module for all constant, server-side data.

This data is typically queried by the client so can be changed without
having the change the client's files (hence the distinction from "constants").
"""
from .enum import *
from .item_template import *
from .quest_objective_template import *
from .quest_template import *
from .starting_items import *
from .starting_locations import *
from .unit_template import *
