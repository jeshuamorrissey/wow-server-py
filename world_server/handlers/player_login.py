import datetime
import enum
from typing import List, Tuple

from pony import orm

from database import world
from world_server import op_code, router, session, system
from world_server.packets import (account_data_times, action_buttons, init_world_states, initial_spells,
                                  login_verify_world, player_login, set_action_button, trigger_cinematic,
                                  tutorial_flags, update_aura_duration)


class ResponseCode(enum.IntEnum):
    FAILED = 0x3A
    FAILED_LOCKED_FOR_TRANSFER = 0x3B
    IN_PROGRESS = 0x38
    SUCCESS = 0x39


@router.Handler(op_code.Client.PLAYER_LOGIN)
@orm.db_session
def handle_player_login(pkt: player_login.ClientPlayerLogin,
                        session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    player = world.Player[pkt.guid_low]
    session.player_id = player.id

    # If this is the first time the player has logged in, send the
    # appropriate cinematic.
    is_first_login = player.last_login is None
    player.last_login = datetime.datetime.utcnow()

    # Build up the INITIAL_SPELLS packet.
    initial_spells_pkt = initial_spells.ServerInitialSpells.build(
        dict(
            spells=[dict(id=ps.spell.id) for ps in player.spells],
            spell_cooldowns=[
                dict(
                    id=ps.spell.id,
                    cast_item_id=0,
                    category=ps.spell.category,
                    cooldown=ps.spell.recovery_time,
                    category_cooldown=ps.spell.category_recovery_time,
                ) for ps in player.spells
            ],
        ))

    actions = [dict(action=0, type=0)] * 120
    for pa in player.action_buttons:
        actions[pa.slot] = dict(
            action=pa.action,
            type=pa.type,
        )

    action_buttons_pkt = action_buttons.ServerActionButtons.build(dict(actions=actions))

    # Add the player to the map.
    update_op, update_pkt = system.Register.Get(system.System.ID.UPDATER).login(player, session)

    # Send information about the player's auras.
    aura_packets = system.Register.Get(system.System.ID.AURA_MANAGER).login(player, session)

    # Make a list of return packets.
    import time
    packets = [
        (
            op_code.Server.LOGIN_VERIFY_WORLD,
            login_verify_world.ServerLoginVerifyWorld.build(
                dict(
                    map=player.map,
                    x=player.x,
                    y=player.y,
                    z=player.z,
                    o=player.o,
                )),
        ),
        (
            op_code.Server.ACCOUNT_DATA_TIMES,
            account_data_times.ServerAccountDataTimes.build(dict(data_times=[0] * 32)),
        ),
        (
            op_code.Server.INIT_WORLD_STATES,
            init_world_states.ServerInitWorldStates.build(dict(
                map=player.map,
                zone=player.zone,
                blocks=[],
            )),
        ),
        (
            op_code.Server.TUTORIAL_FLAGS,
            tutorial_flags.ServerTutorialFlags.build(dict(tutorials=[0] * 8)),
        ),
        (
            op_code.Server.INITIAL_SPELLS,
            initial_spells_pkt,
        ),
        (
            op_code.Server.ACTION_BUTTONS,
            action_buttons_pkt,
        ),
        (
            update_op,
            update_pkt,
        ),
    ]

    packets += aura_packets

    # Trigger a cinematic if this is their first login.
    if is_first_login:
        cinematic = player.race.cinematic_sequence_id
        packets.append((
            op_code.Server.TRIGGER_CINEMATIC,
            trigger_cinematic.ServerTriggerCinematic.build(dict(sequence_id=cinematic)),
        ))

    # TODO: send bindpoint update
    # TODO: send friend list
    # TODO: send ignore list
    # TODO: cast login effect spell
    # TODO: send enchantment durations
    # TODO: send item durations

    # Send some initial setup packets.
    return packets
