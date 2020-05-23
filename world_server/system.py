import enum
from typing import Dict, Text, Type


class System:
    """A system represents a long-running job which manages the background state of the game."""

    class ID(enum.Enum):
        UPDATER = enum.auto()
        AURA_MANAGER = enum.auto()


class Register:
    """Class which acts as a decorator for reigstering system classes."""
    SYSTEMS: Dict[System.ID, System] = {}

    def __init__(self, id: System.ID):
        self._id = id

    def __call__(self, cls: Type):
        if self._id in self.SYSTEMS:
            raise RuntimeError(f'Duplicate definitions of system {self._id}')

        self.SYSTEMS[self._id] = cls()
        return cls

    @classmethod
    def Get(cls, id: System.ID) -> System:
        """Get the given system from storage.
        
        Args:
            id: The ID of the system to get.

        Returns:
            The instance of the system.

        Raises:
            RuntimeError: raised if the system does not exist.
        """
        if id not in cls.SYSTEMS:
            raise RuntimeError(
                f'Request for system {id}, but it is not registered')
        return cls.SYSTEMS[id]
