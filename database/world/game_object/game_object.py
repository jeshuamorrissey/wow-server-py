from pony import orm

from database.db import db
from database.dbc import constants as c


class GameObject(db.Entity):
    id = orm.PrimaryKey(int, auto=True, min=1)
    entry = orm.Optional(int)
    scale = orm.Required(float, default=1.0)

    @property
    def guid(self) -> int:
        return (self.high_guid() << 32) | self.id

    #
    # Class Methods (should be overwritten in children).
    #
    def type_id(self) -> c.TypeID:
        return c.TypeID.OBJECT

    def type_mask(self) -> c.TypeMask:
        return c.TypeMask.OBJECT

    def update_flags(self) -> c.UpdateFlags:
        return c.UpdateFlags.NONE

    def high_guid(self) -> c.HighGUID:
        raise NotImplementedError('GameObjects must have a high GUID.')
