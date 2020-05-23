from pony import orm

from database.db import db


class CinematicSequences(db.Entity):
    id = orm.PrimaryKey(int)
    sound_id = orm.Required(int)
    camera1 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera1_backlink')
    camera2 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera2_backlink')
    camera3 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera3_backlink')
    camera4 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera4_backlink')
    camera5 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera5_backlink')
    camera6 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera6_backlink')
    camera7 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera7_backlink')
    camera8 = orm.Optional('CinematicCamera', reverse='cinematic_sequences_camera8_backlink')

    chr_races_backlink = orm.Set('ChrRaces', reverse='cinematic_sequence')
