import math
from typing import Any, Dict, Optional, Tuple

from pony import orm

from database import game
from database.db import db


class GUID(int):
    """Wrapper class around int which can be used to encode GUID fields.
    
    This will be converted into 2 fields:
      - The first 4 bytes will be the LOW part.
      - The second 4 bytes will be the HIGH part.
    """

    @property
    def low(self) -> int:
        return self & 0xFFFFFFFF

    @property
    def high(self) -> int:
        return self >> 32


class GameObject(db.Entity):
    # This has to be a minimum of 10 because some smaller numbers seem to
    # be reserved (or there is a bug in the client which causes crashes).
    id = orm.PrimaryKey(int, auto=True, min=10)
    scale = orm.Required(float, default=1.0)

    def entry(self) -> Optional[int]:
        return None

    @property
    def guid(self) -> GUID:
        return GUID((self.high_guid() << 32) | self.id)

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
    def type_id(self) -> game.TypeID:
        return game.TypeID.OBJECT

    def type_mask(self) -> game.TypeMask:
        return game.TypeMask.OBJECT

    def update_flags(self) -> game.UpdateFlags:
        return game.UpdateFlags.NONE

    def high_guid(self) -> game.HighGUID:
        raise NotImplementedError('GameObjects must have a high GUID.')

    def num_fields(self) -> int:
        return 0x06

    def update_fields(self) -> Dict[game.UpdateField, Any]:
        """Return a mapping of UpdateField --> Value."""
        of = game.ObjectFields
        return {
            of.GUID: self.guid,
            of.TYPE: self.type_mask(),
            of.ENTRY: self.entry(),
            of.SCALE_X: self.scale,
        }
