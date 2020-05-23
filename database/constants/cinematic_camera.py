from pony import orm

from database.constants import common
from database.db import db


class CinematicCamera(db.Entity):
    id = orm.PrimaryKey(int)
    model = orm.Required(common.SingleString)
    sound_id = orm.Required(int)
    x = orm.Required(float)
    y = orm.Required(float)
    z = orm.Required(float)
    o = orm.Required(float)

    cinematic_sequences_camera1_backlink = orm.Set('CinematicSequences', reverse='camera1')
    cinematic_sequences_camera2_backlink = orm.Set('CinematicSequences', reverse='camera2')
    cinematic_sequences_camera3_backlink = orm.Set('CinematicSequences', reverse='camera3')
    cinematic_sequences_camera4_backlink = orm.Set('CinematicSequences', reverse='camera4')
    cinematic_sequences_camera5_backlink = orm.Set('CinematicSequences', reverse='camera5')
    cinematic_sequences_camera6_backlink = orm.Set('CinematicSequences', reverse='camera6')
    cinematic_sequences_camera7_backlink = orm.Set('CinematicSequences', reverse='camera7')
    cinematic_sequences_camera8_backlink = orm.Set('CinematicSequences', reverse='camera8')
