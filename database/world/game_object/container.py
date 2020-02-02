from pony import orm

from database.dbc import constants as c
from database.world.game_object.item import Item


class Container(Item):
    # Reverse mappings.
    on_slot = orm.Optional('EquippedBag')
