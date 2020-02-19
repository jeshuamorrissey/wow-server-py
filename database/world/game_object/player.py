import datetime
from typing import Dict, Text, Any

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
    last_login = orm.Optional(datetime.datetime)

    # Relationships.
    guild = orm.Optional('Guild')

    # Player location information.
    zone = orm.Required(int)
    map = orm.Required(int)

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

    #
    # Class Methods (should be overwritten in children).
    #
    def type_id(self) -> c.TypeID:
        return c.TypeID.PLAYER

    def type_mask(self) -> c.TypeMask:
        return super(Player, self).type_mask() | c.TypeMask.PLAYER

    def high_guid(self) -> c.HighGUID:
        return c.HighGUID.PLAYER

    def num_fields(self) -> int:
        return 0x06 + 0xB6 + 0x446

    def update_fields(self) -> Dict[c.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        f = c.PlayerFields
        fields = {
            f.DUEL_ARBITER:
            0,
            f.FLAGS:
            0,
            f.GUILDID:
            0,
            f.GUILDRANK:
            0,
            f.BYTES:
            self.skin_color | self.face << 8 | self.hair_style << 16
            | self.hair_color << 24,
            f.BYTES_2:
            self.feature,
            f.BYTES_3:
            self.gender,
            f.DUEL_TEAM:
            0,
            f.GUILD_TIMESTAMP:
            0,
            f.QUEST_LOG_1_1:
            0,
            f.QUEST_LOG_1_2:
            0,
            f.QUEST_LOG_1_3:
            0,
            f.QUEST_LOG_LAST_1:
            0,
            f.QUEST_LOG_LAST_2:
            0,
            f.QUEST_LOG_LAST_3:
            0,
            f.VISIBLE_ITEM_1_CREATOR:
            0,
            f.VISIBLE_ITEM_1_0:
            0,
            f.VISIBLE_ITEM_1_PROPERTIES:
            0,
            f.VISIBLE_ITEM_1_PAD:
            0,
            f.VISIBLE_ITEM_LAST_CREATOR:
            0,
            f.VISIBLE_ITEM_LAST_0:
            0,
            f.VISIBLE_ITEM_LAST_PROPERTIES:
            0,
            f.VISIBLE_ITEM_LAST_PAD:
            0,
            f.INV_SLOT_HEAD:
            0,
            f.PACK_SLOT_1:
            0,
            f.PACK_SLOT_LAST:
            0,
            f.BANK_SLOT_1:
            0,
            f.BANK_SLOT_LAST:
            0,
            f.BANKBAG_SLOT_1:
            0,
            f.BANKBAG_SLOT_LAST:
            0,
            f.VENDORBUYBACK_SLOT_1:
            0,
            f.VENDORBUYBACK_SLOT_LAST:
            0,
            f.KEYRING_SLOT_1:
            0,
            f.KEYRING_SLOT_LAST:
            0,
            f.FARSIGHT:
            0,
            f.COMBO_TARGET:
            0,
            f.XP:
            0,
            f.NEXT_LEVEL_XP:
            0,
            f.SKILL_INFO_1_1:
            0,
            f.CHARACTER_POINTS1:
            0,
            f.CHARACTER_POINTS2:
            0,
            f.TRACK_CREATURES:
            0,
            f.TRACK_RESOURCES:
            0,
            f.BLOCK_PERCENTAGE:
            0,
            f.DODGE_PERCENTAGE:
            0,
            f.PARRY_PERCENTAGE:
            0,
            f.CRIT_PERCENTAGE:
            0,
            f.RANGED_CRIT_PERCENTAGE:
            0,
            f.EXPLORED_ZONES_1:
            0,
            f.REST_STATE_EXPERIENCE:
            0,
            f.COINAGE:
            0,
            f.POSSTAT0:
            0,
            f.POSSTAT1:
            0,
            f.POSSTAT2:
            0,
            f.POSSTAT3:
            0,
            f.POSSTAT4:
            0,
            f.NEGSTAT0:
            0,
            f.NEGSTAT1:
            0,
            f.NEGSTAT2:
            0,
            f.NEGSTAT3:
            0,
            f.NEGSTAT4:
            0,
            f.RESISTANCEBUFFMODSPOSITIVE:
            0,
            f.RESISTANCEBUFFMODSNEGATIVE:
            0,
            f.MOD_DAMAGE_DONE_POS:
            0,
            f.MOD_DAMAGE_DONE_NEG:
            0,
            f.MOD_DAMAGE_DONE_PCT:
            0,
            f.BYTES:
            0,
            f.AMMO_ID:
            0,
            f.SELF_RES_SPELL:
            0,
            f.PVP_MEDALS:
            0,
            f.BUYBACK_PRICE_1:
            0,
            f.BUYBACK_PRICE_LAST:
            0,
            f.BUYBACK_TIMESTAMP_1:
            0,
            f.BUYBACK_TIMESTAMP_LAST:
            0,
            f.SESSION_KILLS:
            0,
            f.YESTERDAY_KILLS:
            0,
            f.LAST_WEEK_KILLS:
            0,
            f.THIS_WEEK_KILLS:
            0,
            f.THIS_WEEK_CONTRIBUTION:
            0,
            f.LIFETIME_HONORABLE_KILLS:
            0,
            f.LIFETIME_DISHONORABLE_KILLS:
            0,
            f.YESTERDAY_CONTRIBUTION:
            0,
            f.LAST_WEEK_CONTRIBUTION:
            0,
            f.LAST_WEEK_RANK:
            0,
            f.BYTES2:
            0,
            f.WATCHED_FACTION_INDEX:
            0,
            f.COMBAT_RATING_1:
            0,
        }

        return {**super(Player, self).update_fields(), **fields}
