from typing import List, Tuple

from pony import orm

from database import world
from world_server import op_code, router, session
from world_server.packets import pet_name_query


@router.Handler(op_code.Client.PET_NAME_QUERY)
@orm.db_session
def handler(pkt: pet_name_query.ClientPetNameQuery, session: session.Session) -> List[Tuple[op_code.Server, bytes]]:
    pet = world.Pet.get(id=world.GUID(pkt.pet_guid).low)
    if not pet:
        return []

    return [(
        op_code.Server.PET_NAME_QUERY,
        pet_name_query.ServerPetNameQuery.build(
            dict(
                number=pkt.pet_number,
                name=pet.name,
                name_timestamp=int(pet.name_timestamp.timestamp()),
            )),
    )]
