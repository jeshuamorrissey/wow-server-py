import enum
import os
from typing import Text

from pony import orm

from database import common

# The main, single database used by this application.
#
# The database should be configured separately in a main function.
db = orm.Database()


def SetupDatabase(db_file: Text, clear_database: bool = False):
    # Import all of the DBC entities.
    from database.dbc.char_start_outfit import CharStartOutfit
    from database.dbc.chr_start_locations import ChrStartLocation
    from database.dbc.data import LoadDBC
    from database.dbc.dbc import AnimationData, AreaPOI, AreaTrigger, AttackAnimKits, AttackAnimTypes, AuctionHouse, BankBagSlotPrices, Faction, Languages, CreatureType, Spell, CinematicCamera, CinematicSequences, ChrRaces
    from database.dbc.item_template import ItemTemplate
    from database.dbc.profession import Profession
    from database.dbc.quest_template import QuestTemplate, Objective
    from database.dbc.spell_template import SpellTemplate
    from database.dbc.unit_template import UnitTemplate

    # Import all of the World entities.
    from database.world.account import Account
    from database.world.aura import Aura
    from database.world.enchantment import Enchantment
    from database.world.game_object.container import Container
    from database.world.game_object.game_object import GameObject
    from database.world.game_object.item import Item, ItemEnchantment
    from database.world.game_object.pet import Pet
    from database.world.game_object.player import EquippedItem, BackpackItem, EquippedBag, BankItem, BankBag, VendorBuybackItem, KeyringItem, PlayerProfession, PlayerSkill, Player
    from database.world.game_object.unit import Unit
    from database.world.guild import Guild, GuildMembership
    from database.world.quest import Quest, ObjectiveProgress
    from database.world.realm import Realm

    # Clear the database if requested.
    if clear_database and db_file != ':memory:' and os.path.exists(db_file):
        os.remove(db_file)

    # Connect to the SQLite database.
    db.bind(provider='sqlite', filename=db_file, create_db=True)
    db.provider.converter_classes.append((enum.Enum, common.EnumConverter))
    db.generate_mapping(check_tables=False)

    # Clear all of the WORLD database tables.
    for cls in [
            Account,
            BackpackItem,
            EquippedBag,
            EquippedItem,
            BankBag,
            BankItem,
            KeyringItem,
            VendorBuybackItem,
            GameObject,
            Guild,
            Realm,
            Aura,
            GuildMembership,
            Quest,
            ObjectiveProgress,
            PlayerProfession,
            PlayerSkill,
    ]:
        cls.drop_table(with_all_data=True)

    # Now actually make the dables.
    db.create_tables()

    # Setup the DBC.
    LoadDBC()
