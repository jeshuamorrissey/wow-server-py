import enum
from typing import Dict, List, Optional

from construct import (Array, Bytes, Const, Enum, Float32l, GreedyBytes,
                       GreedyRange, If, Int8ul, Int32ul, Int64ul, Rebuild,
                       Struct, Switch)
from pony import orm

from database.dbc import constants as c
from database.world.game_object.container import Container
from database.world.game_object.game_object import GameObject
from database.world.game_object.item import Item
from database.world.game_object.player import Player
from database.world.game_object.unit import Unit
from world_server import session, system
from world_server.packets import compressed_update_object, update_object


@system.Register(system.System.ID.UPDATER)
class Updater(system.System):
    def __init__(self):
        self.players: Dict[int, session.Session] = {}

        # Caches to keep track of what players have seen.
        self._update_fields_cache: Dict[int, dict] = {}
        self._movement_update_cache: Dict[int, dict] = {}

    def _make_movement_update(self, game_object: GameObject) -> Optional[dict]:
        """Return either a FullMovementUpdate or PositionMovementUpdate.

        The returned dictionary can be used to construct the appropriate
        update for the given game object.

        Args:
            game_object: The object to build the update for.

        Returns:
            A dictionary for constructing the movement update. If the object
            has no movement update, then return None.
        """
        if c.UpdateFlags.LIVING in game_object.update_flags():
            # TODO FullMovementUpdate
            return None
        elif c.UpdateFlags.HAS_POSITION in game_object.update_flags():
            return dict(
                x=game_object.x,
                y=game_object.y,
                z=game_object.z,
                o=game_object.o,
            )

        return None

    # def _make_full_update_block(self, player: Player,
    #                             game_object: GameObject) -> dict:
    #     """Make a FullUpdateBlock struct dictionary."""
    #     return dict(
    #         guid=
    #     )

    # def _make_values_update(
    #         self,
    #         player: Player,
    #         game_object: GameObject,
    # ) -> dict:
    #     return {}

    # def _make_movement_update(
    #         self,
    #         player: Player,
    #         game_object: GameObject,
    # ) -> dict:
    #     return {}

    # def _make_update_block(
    #         self,
    #         player: Player,
    #         game_object: GameObject,
    # ) -> Optional[dict]:
    #     # Generate the updates. This will only return fields which are different
    #     # from the cache, but will not update the cache.
    #     movement_update = self._make_movement_update(player, game_object)
    #     values_update = self._make_values_update(player, game_object)

    #     # Work out the update type.
    #     update_type = update_object.UpdateType.VALUES
    #     if not movement_update:
    #         if not values_update:
    #             return None  # no update to make
    #         else:
    #             update_type = update_object.UpdateType.VALUES
    #     else:
    #         if player.id not in self._fields_update_cache:
    #             update_type = update_object.UpdateType.CREATE_OBJECT
    #         else:
    #             update_type = update_object.UpdateType.MOVEMENT

    #     if update_type == update_object.UpdateType.VALUES:
    #         update_block = dict(
    #             guid=dict(
    #                 mask=1,
    #                 bytes=[1],
    #             ),
    #             update=values_update,
    #         )
    #     else:
    #         update_block = dict(
    #             guid=dict(
    #                 mask=1,
    #                 bytes=[1],
    #             ),
    #             object_type=...,
    #             flags=...,
    #         )

    #     # Check the update cache to see whether we are making the object
    #     # or just updating the values.
    #     block = dict(
    #         update_type=update_type,
    #         update_block=update_block,
    #     )

    #     return block

    # def _make_update_object(
    #         self,
    #         player: Player,
    #         game_objects: List[GameObject],
    # ) -> bytes:
    #     update_blocks = []
    #     for o in game_objects:
    #         update_block = self._make_update_block(player, o)
    #         if update_block:
    #             update_blocks.append(update_block)

    #     return update_object.ServerUpdateObject.build(
    #         is_transport=0,  # TODO
    #         blocks=update_blocks,
    #     )

    @orm.db_session
    def login(self, player: Player, session: session.Session):
        """Mark the given player as logged in.

        This will cause object updates to be sent to them immediately.

        Args:
            player: The player to log in.
            session: The session the player can be contacted on.
        """
        session.log.info(
            f'Updater: registered new player {player.name} (id = {player.id})')
        self.players[player.id] = session

        # Send self UPDATE_OBJECT packet.
        # TODO

        # Send UPDATE_OBJECT packets for all nearby objects.
        # TODO

    @orm.db_session
    def update_object(self, game_object: GameObject):
        """Send updates to the given object to all parties.

        Args:
            game_object: The object which is being updated.
        """
        pass
