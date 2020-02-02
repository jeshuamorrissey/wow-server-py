from typing import Dict, Text

from pony import orm

from database.db import db
from database.dbc import constants as c
from database.dbc.char_start_outfit import CharStartOutfit
from database.dbc.chr_start_locations import ChrStartLocation
from database.dbc.item_template import ItemTemplate
from database.world.account import Account
from database.world.game_object import unit
from database.world.game_object.item import Item
from database.world.realm import Realm


class EquippedItem(db.Entity):
    """Mapping table to store details about which items are equipped."""
    owner = orm.Required('Player')
    slot = orm.Required(c.EquipmentSlot)
    item = orm.Required('Item')

    orm.PrimaryKey(owner, slot)


class BackpackItem(db.Entity):
    """Mapping table to store details about which items are in the backpack.

    The backpack is the default bag you always have available.
    """
    owner = orm.Required('Player')
    slot = orm.Required(int, min=0, max=15)
    item = orm.Required('Item')

    orm.PrimaryKey(owner, slot)


class EquippedBag(db.Entity):
    """Mapping table to store details about which bags are equipped."""
    owner = orm.Required('Player')
    slot = orm.Required(int, min=0, max=3)
    container = orm.Required('Container')

    orm.PrimaryKey(owner, slot)


class Player(unit.Unit):
    # General character information.
    account = orm.Required('Account')
    realm = orm.Required('Realm')
    name = orm.Required(str, unique=True)

    # Relationships.
    guild = orm.Optional('Guild')

    # Player location information.
    zone = orm.Required(int)
    map = orm.Required(int)

    # Pet.
    pet = orm.Optional('Unit')

    # Inventory.
    equipment = orm.Set(EquippedItem)
    backpack_items = orm.Set(BackpackItem)
    bags = orm.Set(EquippedBag)

    # Game-object specific information.
    skin_color = orm.Required(int, default=0)
    face = orm.Required(int, default=0)
    hair_style = orm.Required(int, default=0)
    hair_color = orm.Required(int, default=0)
    feature = orm.Required(int, default=0)

    # Player flags.
    is_ghost = orm.Required(bool, default=False)
    hide_helm = orm.Required(bool, default=False)
    hide_cloak = orm.Required(bool, default=False)

    def equipment_map(self) -> Dict[c.EquipmentSlot, Item]:
        """Return a mapping of equipment slot --> equipped item.
        
        This is useful in situations where we have to fully specify the
        equipment (even if there is no equipment).

        Returns:
            A mapping from equipment slot --> item equipped in that slot.
        """
        return {eq.slot: eq.item for eq in self.equipment}

    @classmethod
    def New(
            cls,
            account: Account,
            realm: Realm,
            name: Text,
            race: c.Race,
            class_: c.Class,
            gender: c.Gender,
            **kwargs,
    ) -> 'Player':
        """Create a new player and return it.

        Args:
            account: The account the player belongs to.
            realm: The realm the player resides on.
            name: The player's name.
            race: The player's race.
            class_: The player's class.
            gender: The player's gender.
            **kwargs: Additional arguments to pass to the Player constructor.

        Returns:
            The newly created character.
        """
        starting_location = ChrStartLocation.get(race=race)
        starting_items = CharStartOutfit.get(race=race,
                                             class_=class_,
                                             gender=gender)
        player = Player(
            account=account,
            realm=realm,
            name=name,
            level=1,
            race=race,
            class_=class_,
            gender=gender,
            x=starting_location.x,
            y=starting_location.y,
            z=starting_location.z,
            o=starting_location.o,
            zone=starting_location.zone,
            map=starting_location.map,
            **kwargs,
        )

        for equipment in starting_items.equipment:
            EquippedItem(
                owner=player,
                slot=c.EquipmentSlot[equipment['equipment_slot']],
                item=Item(base_item=ItemTemplate[equipment['entry']]),
            )

        for i, entry in enumerate(starting_items.items):
            BackpackItem(
                owner=player,
                slot=i,
                item=Item(base_item=ItemTemplate[entry]),
            )

        return player

    @property
    def high_guid(self) -> int:
        return 0
