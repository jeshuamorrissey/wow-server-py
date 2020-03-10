from pony import orm

from database.db import db
from database.constants import common


class AnimationData(db.Entity):
    id = orm.PrimaryKey(int)
    name = orm.Required(common.SingleEnumString)
    weapon_flags = orm.Required(int)
    body_flags = orm.Required(int)
    flags = orm.Required(int)
    fallback = orm.Optional('AnimationData', reverse='fallback_backlink')
    previous = orm.Optional('AnimationData', reverse='previous_backlink')

    fallback_backlink = orm.Set('AnimationData', reverse='fallback')
    previous_backlink = orm.Set('AnimationData', reverse='previous')
