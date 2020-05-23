import logging
import threading
import time
from typing import Dict, List, Tuple

from pony import orm

from database import constants, game, world
from world_server import op_code, system
from world_server.packets import update_aura_duration
from world_server.session import Session


@system.Register(system.System.ID.AURA_MANAGER)
class AuraManager(system.System):
    """System which manages applied auras."""
    def __init__(self):
        self.aura_available_cond = threading.Condition()
        self._players: Dict[int, Session] = {}

    @orm.db_session
    def _get_next_wakeup(self):
        return orm.min(a.expiry_time for a in world.Aura)

    @orm.db_session
    def _get_duration_update_packet(self, aura: world.Aura) -> bytes:
        return update_aura_duration.ServerUpdateAuraDuration.build(
            dict(
                slot=aura.slot,
                duration=(aura.expiry_time - int(time.time())) * 1000,
            ))

    @orm.db_session
    def _send_aura_duration_update(self, aura: world.Aura):
        pkt = self._get_duration_update_packet(aura)
        self._players[aura.applied_to.id].send_packet(
            op_code.Server.UPDATE_AURA_DURATION, pkt)

    @orm.db_session
    def login(self, player: world.Player,
              session: Session) -> List[Tuple[op_code.Server, bytes]]:
        self._players[player.id] = session

        # Craft packets for each aura the player has. Don't actually send them, let the
        # login manager do that.
        packets = []
        for aura in (a for a in world.Aura.select() if a.applied_to == player):
            packets.append((
                op_code.Server.UPDATE_AURA_DURATION,
                self._get_duration_update_packet(aura),
            ))

        return packets

    @orm.db_session
    def process_auras(self):
        now = int(time.time())
        for aura in world.Aura.select():
            if aura.expiry_time < now:
                print(f'Aura {aura.applied_to}:{aura.slot} expired!')
                applied_to = aura.applied_to
                aura.delete()

                system.Register.Get(
                    system.System.ID.UPDATER).update_object(applied_to)

    @orm.db_session
    def create_aura(self, caster: world.Unit, target: world.Unit,
                    spell: constants.Spell):
        # Find the next aura slot on `target`.
        auras = {aura.slot: aura for aura in world.Aura.select()}
        slot = None
        for i in range(48):
            if i not in auras:
                slot = i

        if slot is None:
            raise RuntimeError('Too many auras :(')

        world.Aura(
            slot=slot,
            applied_to=target,
            base_spell=spell,
            expiry_time=int(time.time()) + 10,  # TODO
        )

        self.aura_available_cond.notify()

    def run(self):
        """Run the aura manager. This will take control of the current thread."""
        logging.debug('Starting aura manager')
        while True:
            # Go back to sleep until the next wakeup.
            next_wakeup = self._get_next_wakeup()
            if not next_wakeup:
                with self.aura_available_cond:
                    self.aura_available_cond.wait()
                continue

            now = int(time.time())
            if next_wakeup and now < next_wakeup:
                time.sleep(next_wakeup - now)

            # Process active auras.
            self.process_auras()
