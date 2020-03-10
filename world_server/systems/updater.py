import enum
from typing import Dict, Iterable, Optional, Tuple

from construct import (Array, Bytes, Const, Enum, Float32l, GreedyBytes, GreedyRange, If, Int8ul, Int32ul, Int64ul,
                       Rebuild, Struct, Switch)
from pony import orm

from database import constants, game, world
from world_server import config, op_code, session, system
from world_server.packets import compressed_update_object, update_object


class PlayerUpdateCache:
    """PlayerUpdateCache is a per-player cache for update values.

    Each cache contains a map for values & movement updates for each object
    (based on ID).
    """

    def __init__(self):
        self.values_updates: Dict[int, dict] = {}
        self.movement_updates: Dict[int, dict] = {}


@system.Register(system.System.ID.UPDATER)
class Updater(system.System):

    def __init__(self):
        self.players: Dict[int, session.Session] = {}

        # Caches to keep track of what players have seen.
        self._update_cache: Dict[int, PlayerUpdateCache] = {}

    def _make_movement_update(self, game_object: world.GameObject) -> Optional[dict]:
        """Return either a FullMovementUpdate or PositionMovementUpdate.

        The returned dictionary can be used to construct the appropriate
        update for the given game object.

        Args:
            game_object: The object to build the update for.

        Returns:
            A dictionary for constructing the movement update. If the object
            has no movement update, then return None.
        """
        # TODO: do a proper movement update with all data
        if game.UpdateFlags.LIVING in game_object.update_flags():
            return dict(
                flags=game.MovementFlags.NONE,
                time=0,
                x=game_object.x,
                y=game_object.y,
                z=game_object.z,
                o=game_object.o,
                transport=None,
                swimming=None,
                last_fall_time=0,
                falling=None,
                spline_elevation=None,
                speed=dict(
                    walk=1.0,
                    run=1.0,
                    run_backward=1.0,
                    swim=1.0,
                    swim_backward=1.0,
                    turn=1.0,
                ),
                spline_update=None,
            )
        elif game.UpdateFlags.HAS_POSITION in game_object.update_flags():
            return dict(
                x=game_object.x,
                y=game_object.y,
                z=game_object.z,
                o=game_object.o,
            )

        return None

    def _make_update_block(self, player: world.Player, game_object: world.GameObject) -> dict:
        """Return a FullUpdateBlock, ValuesUpdateBlock or OutOfRangeUpdateBlock.

        Args:  
            player: The player this update is being sent do.
            game_object: The game object this update is for.

        Returns:
            A dictionary which can be used to construct an UpdateBlock struct.
        """
        player_cache = self._update_cache[player.id]

        # Generate the updates for the player.
        movement_update = self._make_movement_update(game_object)
        values_update = game_object.update_fields()

        # Get the cached updates.
        last_movement_update = player_cache.movement_updates.get(game_object.id, None)
        last_values_update = player_cache.values_updates.get(game_object.id, {})

        # Work out the delta in the values update.
        values_update_diff = {k: v for k, v in values_update.items() if last_values_update.get(k, None) != v}

        # Work out the update type.
        update_type = None
        if game_object.id not in player_cache.values_updates:
            # We need to create the object.
            update_type = game.UpdateType.CREATE_OBJECT
        else:
            if movement_update != last_movement_update:
                # Movement update required.
                update_type = game.UpdateType.MOVEMENT
            else:
                if values_update_diff:
                    # No movement update, only a values update.
                    update_type = game.UpdateType.VALUES
                else:
                    # Shortcut: there is no update to perform.
                    return {}

        # Update the cache.
        if movement_update:
            player_cache.movement_updates[game_object.id] = movement_update
        player_cache.values_updates[game_object.id] = values_update

        if update_type == game.UpdateType.VALUES:
            return dict(
                update_type=update_type,
                update_block=dict(
                    guid=game_object.guid,
                    update=dict(
                        num_fields=game_object.num_fields(),
                        fields=values_update_diff,
                    ),
                ),
            )

        update_flags = game_object.update_flags()
        if player.guid == game_object.guid:
            update_flags |= game.UpdateFlags.SELF

        return dict(
            update_type=update_type,
            update_block=dict(
                guid=game_object.guid,
                object_type=game_object.type_id(),
                flags=update_flags,
                movement_update=self._make_movement_update(game_object),
                high_guid=None,
                victim_guid=None,
                world_time=None,
                update_fields=dict(
                    num_fields=game_object.num_fields(),
                    fields=game_object.update_fields(),
                ),
            ),
        )

    def _make_update_object(
            self,
            player: world.Player,
            game_objects: Iterable[world.GameObject],
    ) -> Tuple[op_code.Server, bytes]:
        out_of_range_guids = []
        update_blocks = []
        for o in game_objects:
            if player.distance_to(o) > config.MAX_UPDATE_DISTANCE:
                out_of_range_guids.append(o.guid)
            else:
                update_block = self._make_update_block(player, o)
                if update_block:
                    update_blocks.append(update_block)

        # Make an update block for OUT_OF_RANGE updates.
        if out_of_range_guids:
            update_blocks.append(
                dict(
                    update_type=game.UpdateType.OUT_OF_RANGE_OBJECTS,
                    update_block=dict(
                        n_guids=len(out_of_range_guids),
                        guids=out_of_range_guids,
                    ),
                ))

        update_data = dict(
            n_blocks=len(update_blocks),
            is_transport=0,  # TODO
            blocks=update_blocks,
        )

        op = op_code.Server.UPDATE_OBJECT
        update_object_pkt = update_object.ServerUpdateObject.build(update_data)
        if len(update_object_pkt) > config.MAX_UPDATE_OBJECT_PACKET_SIZE:
            op = op_code.Server.COMPRESSED_UPDATE_OBJECT
            update_object_pkt = compressed_update_object.ServerCompressedUpdateObject.build(
                dict(uncompressed_size=len(update_object_pkt), data=update_data))

        return (op, update_object_pkt)

    @orm.db_session
    def login(self, player: world.Player, session: session.Session):
        """Mark the given player as logged in.

        This will cause object updates to be sent to them immediately.

        Args:
            player: The player to log in.
            session: The session the player can be contacted on.
        """
        session.log.info(f'Updater: registered new player {player.name} (id = {player.id})')
        self.players[player.id] = session
        self._update_cache[player.id] = PlayerUpdateCache()

        op, update_object_pkt = self._make_update_object(
            player,
            (o for o in world.GameObject.select() if o.distance_to(player) < config.MAX_UPDATE_DISTANCE),
        )

        return op, update_object_pkt

    @orm.db_session
    def logout(self, player: world.Player):
        """Mark the given player as logged in.

        This will cause object updates to be sent to them immediately.

        Args:
            player: The player to log in.
            session: The session the player can be contacted on.
        """
        self.players[player.id].log.info(f'Updater: player logout {player.name} (id = {player.id})')
        del self.players[player.id]
        del self._update_cache[player.id]

        # Send DESTROY_OBJECT packets for this player to all other players.
        # TODO

    @orm.db_session
    def update_object(self, game_object: world.GameObject):
        """Send updates for the given object to all parties.

        Args:
            game_object: The object which is being updated.
        """
        for player_id, session in self.players.items():
            op, update_object_pkt = self._make_update_object(world.GameObject[player_id], [game_object])
            session.send_packet(op, update_object_pkt)
