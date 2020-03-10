import argparse
import datetime
import enum
import logging
import os
import threading
import time
from typing import Text

import coloredlogs
from pony import orm

import login_server.handlers  # register handlers
import login_server.packets  # register packet formats
import world_server.handlers  # register handlers
import world_server.packets  # register packet formats
import world_server.systems  # register systems
from common import server
from database import constants, db, game, world
from login_server import router as login_router
from login_server import session as login_session
from world_server import router as world_router
from world_server import session as world_session
from world_server import system


def setup_db(args: argparse.Namespace):
    db.SetupDatabase(args.db_file, clear_database=args.reset_database, clear_dynamic_database=args.reset_world_database)

    # Generate some test data.
    # Clear the world database tables so they can be created again.
    if args.reset_world_database:
        with orm.db_session:
            account = world.Account.New(username='jeshua', password='jeshua')
            realm = world.Realm(name='Brisbane', hostport=f'{args.host}:{args.world_port}')
            guild = world.Guild()
            jeshua = world.Player.New(
                id=10,
                account=account,
                realm=realm,
                name='Jeshua',
                race=constants.EChrRaces.HUMAN,
                class_=constants.EChrClasses.WARRIOR,
                gender=game.Gender.MALE,
                last_login=datetime.datetime.now(),
                base_health=100,  # TODO: use ChrBaseStats
                base_power=100,  # TODO: use ChrBaseStats
                strength=5,
                agility=5,
                stamina=5,
                intellect=5,
                spirit=5,
                level=20,
                rested_xp=5000,
                money=10000,
                explored_zones=range(game.MAX_EXPLORED_ZONES),
            )

            bag = world.Container.New(base_item=game.ItemTemplate[14156])
            world.EquippedBag(
                owner=jeshua,
                slot=0,
                container=bag,
            )

            world.ContainerItem(
                container=bag,
                item=world.Item.New(base_item=game.ItemTemplate[14156]),
                slot=0,
            )

            world.PlayerSkill(
                player=jeshua,
                skill=game.SkillType.AXES,
                level=10,
                bonus=10,
            )

            world.GuildMembership(
                player=jeshua,
                guild=guild,
                rank=1,
            )

            world.Quest.New(jeshua, game.QuestTemplate.get(title='With Duration'))
            world.Quest.New(jeshua, game.QuestTemplate.get(title='Without Duration'))

            world.Aura(
                slot=0,
                applied_to=jeshua,
                base_spell=constants.Spell[1459],
                expiry_time=int(time.time()) + 6000,
            )

            base_unit = game.UnitTemplate.get(Name='Young Nightsaber')
            world.Pet(
                base_unit=base_unit,
                level=1,
                race=0,
                class_=base_unit.UnitClass,
                gender=game.Gender.FEMALE,
                team=jeshua.team,
                x=jeshua.x + 2,
                y=jeshua.y + 2,
                z=jeshua.z,
                o=jeshua.o,
                summoner=jeshua,
                created_by=jeshua,
                base_health=100,
                base_power=100,
            )

            base_unit = game.UnitTemplate.get(Name='Lady Sylvanas Windrunner')
            world.Unit(
                base_unit=base_unit,
                level=55,
                race=0,
                class_=base_unit.UnitClass,
                gender=game.Gender.MALE,
                x=jeshua.x + 2,
                y=jeshua.y - 2,
                z=jeshua.z,
                o=jeshua.o,
                base_health=100,
                base_power=100,
                team=game.Team.HORDE,
                npc_ranged=game.ItemTemplate.get(name='Soulstring'),
                sheathed_state=game.SheathedState.RANGED,
            )


def main(args: argparse.Namespace):
    # Load the database.
    setup_db(args)

    # Create the packet handling threads.
    auth_thread = threading.Thread(target=server.run,
                                   kwargs=dict(
                                       name='AUTH',
                                       host=args.host,
                                       port=args.auth_port,
                                       session_type=login_session.Session,
                                       packet_formats=login_router.ClientPacket.ROUTES,
                                       handlers=login_router.Handler.ROUTES,
                                   ))

    world_thread = threading.Thread(target=server.run,
                                    kwargs=dict(
                                        name='WORLD',
                                        host=args.host,
                                        port=args.world_port,
                                        session_type=world_session.Session,
                                        packet_formats=world_router.ClientPacket.ROUTES,
                                        handlers=world_router.Handler.ROUTES,
                                    ))

    # Start the aura manager.
    aura_manager_thread = threading.Thread(target=system.Register.Get(system.System.ID.AURA_MANAGER).run)
    aura_manager_thread.start()

    auth_thread.start()
    world_thread.start()

    aura_manager_thread.join()
    auth_thread.join()
    world_thread.join()


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(description='Server to handle the initial login connection.')
    argument_parser.add_argument('--auth_port',
                                 type=int,
                                 default=5000,
                                 help='The port to list for AUTH connections on.')
    argument_parser.add_argument('--world_port',
                                 type=int,
                                 default=5001,
                                 help='The port to list for WORLD connections on.')
    argument_parser.add_argument('--host', type=str, default='127.0.0.1', help='The host to list for connections on.')
    argument_parser.add_argument('--db_file',
                                 type=str,
                                 default='/tmp/wow_server.db',
                                 help='The file to store the World database in.')
    argument_parser.add_argument('--reset_database',
                                 action='store_true',
                                 help='If True, the DBC database will be reloaded.')
    argument_parser.add_argument('--reset_world_database',
                                 action='store_true',
                                 help='If True, the World database will be reloaded.')
    argument_parser.set_defaults(reset_database=False, reset_world_database=True)
    coloredlogs.install(level='DEBUG')

    main(argument_parser.parse_args())
