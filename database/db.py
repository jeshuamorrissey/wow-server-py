import enum
import os
from typing import Text

from pony import orm

from database import common, data

# The main, single database used by this application.
#
# The database should be configured separately in a main function.
db = orm.Database()


def SetupDatabase(db_file: Text, clear_database: bool = False):
    # Import database entities.
    from database import constants
    from database import game
    from database import world

    # Clear the database if requested.
    if clear_database and db_file != ':memory:' and os.path.exists(db_file):
        os.remove(db_file)

    # Connect to the SQLite database.
    db.bind(provider='sqlite', filename=db_file, create_db=True)
    db.provider.converter_classes.append((enum.Enum, common.EnumConverter))
    db.generate_mapping(check_tables=False)

    # Clear all of the WORLD database tables.
    # for cls in [
    #         Account,
    #         BackpackItem,
    #         EquippedBag,
    #         EquippedItem,
    #         BankBag,
    #         BankItem,
    #         KeyringItem,
    #         VendorBuybackItem,
    #         GameObject,
    #         Guild,
    #         Realm,
    #         Aura,
    #         GuildMembership,
    #         Quest,
    #         ObjectiveProgress,
    #         PlayerProfession,
    #         PlayerSkill,
    # ]:
    #     cls.drop_table(with_all_data=True)

    # Now actually make the dables.
    db.create_tables()

    # Setup the DBC.
    data.load_constants(db)
