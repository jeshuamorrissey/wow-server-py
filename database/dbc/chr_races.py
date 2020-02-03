from pony import orm

from database.db import db
from database.dbc import constants as c


class ChrRaces(db.Entity):
    race = orm.PrimaryKey(c.Race)

    # TODO: sort these fields, copied from ChrRaces.dbc
    flags = orm.Required(int)
    faction_template_id = orm.Required(int)
    exploration_sound_id = orm.Required(int)
    male_display_id = orm.Required(int)
    female_display_id = orm.Required(int)
    client_prefix = orm.Required(str)
    speed = orm.Required(float)
    base_language_id = orm.Required(int)
    creature_type_id = orm.Required(int)
    login_effect_spell_id = orm.Required(int)
    combat_stun_spell_id = orm.Required(int)
    res_sickness_spell_id = orm.Required(int)
    splash_sound_id = orm.Required(int)
    starting_taxi_nodes = orm.Required(int)
    client_file_string = orm.Required(str)
    cinematic_sequence_id = orm.Required(int)
    name = orm.Required(str)
    name_flags = orm.Required(int)
    facial_hair_customization_0 = orm.Required(str)
    facial_hair_customization_1 = orm.Required(str)
    hair_customization = orm.Required(str)
