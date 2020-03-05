from typing import List, Tuple

from pony import orm

from common import srp
from database.dbc import constants as c
from database.world.account import Account
from world_server import op_code, router, session
from world_server.packets import char_enum


@router.Handler(op_code.Client.CHAR_ENUM)
@orm.db_session
def handle_char_enum(pkt: char_enum.ClientCharEnum, session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    account = Account[session.account_name]

    characters = []
    for character in account.characters:
        guild_id = character.guild_membership.guild.id if character.guild_membership else 0

        # Build up the equipment list. This list has to be in order, even if
        # the items aren't actually in order.
        equipment_map = character.equipment_map()
        equipment = []
        for slot in c.EquipmentSlot:
            item = equipment_map.get(slot, None)
            if item:
                equipment.append(dict(display_id=item.base_item.displayid, inventory_type=item.base_item.InventoryType))
            else:
                equipment.append(dict(display_id=0, inventory_type=0))

        pet = dict(display_id=0, level=0, family=0)
        if character.summon:
            pet = dict(
                display_id=character.summon.base_unit.ModelId1,
                level=character.summon.level,
                family=character.summon.base_unit.Family,
            )

        # Make the enum data.
        characters.append(
            dict(
                guid=character.id,
                name=character.name,
                race=character.race,
                class_=character.class_,
                gender=character.gender,
                appearance=dict(
                    skin=character.skin_color,
                    face=character.face,
                    hair_style=character.hair_style,
                    hair_color=character.hair_color,
                    feature=character.feature,
                ),
                level=character.level,
                location=dict(
                    zone=character.zone,
                    map=character.map,
                    x=character.x,
                    y=character.y,
                    z=character.z,
                ),
                guild_id=guild_id,
                flags=dict(
                    is_ghost=character.is_ghost,
                    hide_helm=character.hide_helm,
                    hide_cloak=character.hide_cloak,
                ),
                pet=pet,
                items=equipment,
            ))

    return [(
        op_code.Server.CHAR_ENUM,
        char_enum.ServerCharEnum.build(dict(characters=characters)),
    )]
