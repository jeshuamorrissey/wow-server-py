from pony import orm

from database.db import db
from database.constants import common


class ChrRaces(db.Entity):
    id = orm.PrimaryKey(int)
    flags = orm.Required(int)
    faction = orm.Required('Faction', reverse='chr_races_backlink')
    exploration_sound_id = orm.Required(int)
    male_display_id = orm.Required(int)
    female_display_id = orm.Required(int)
    client_prefix = orm.Required(common.SingleString)
    mount_scale = orm.Required(float)
    base_language = orm.Required('Languages', reverse='chr_races_backlink')
    creature_type = orm.Required('CreatureType', reverse='chr_races_backlink')
    login_effect = orm.Required('Spell', reverse='chr_races_login_effect_backlink')
    combat_stun = orm.Required('Spell', reverse='chr_races_combat_stun_backlink')
    res_sickness = orm.Required('Spell', reverse='chr_races_res_sickness_backlink')
    splash_sound_id = orm.Required(int)
    starting_taxi_nodes = orm.Required(int)
    client_file_string = orm.Required(common.SingleString)
    cinematic_sequence = orm.Optional('CinematicSequences', reverse='chr_races_backlink')
    name = orm.Required(common.MultiEnumString)
    facial_hair_customization_male = orm.Required(common.SingleString)
    facial_hair_customization_female = orm.Required(common.SingleString)
    hair_customization = orm.Required(common.SingleString)
