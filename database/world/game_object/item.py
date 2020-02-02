from pony import orm

from database.dbc import constants as c
from database.world.game_object.game_object import GameObject


class Item(GameObject):
    base_item = orm.Required('ItemTemplate')

    # Reverse mappings.
    equipped_by = orm.Optional('EquippedItem')
