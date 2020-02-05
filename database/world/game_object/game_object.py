from typing import Tuple, Optional, Dict, Any

from pony import orm

import math

from database.db import db
from database.dbc import constants as c


class GameObject(db.Entity):
    id = orm.PrimaryKey(int, auto=True, min=1)
    entry = orm.Optional(int)
    scale = orm.Required(float, default=1.0)

    @property
    def guid(self) -> int:
        return (self.high_guid() << 32) | self.id

    def position(self) -> Tuple[float, float, float]:
        """Get the current position of the object.

        All objects either have a position, or have a parent who has a 
        position, so a result from this should always be possible.

        Returns:
            A 3-tuple of floats (x, y, z).
        """
        raise NotImplementedError('GameObjects must have a position')

    def distance_to(self, other: 'GameObject') -> float:
        """Calculate the distance between this and another game object.

        Args:
            other: The other game object.

        Returns:
            The distance between them as a float.
        """
        x1, y1, z1 = self.position()
        x2, y2, z2 = other.position()
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

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

    def num_fields(self) -> int:
        return 0x06

    def update_fields(self) -> Dict[c.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        of = c.ObjectFields
        return {
            of.GUID_LOW: self.id,
            of.GUID_HIGH: self.high_guid(),
            of.TYPE: self.type_mask(),
            of.ENTRY: self.entry,
            of.SCALE_X: self.scale,
        }
