import sys

import pytest

from database import world, enums, game, constants
from world_server import op_code
from world_server.handlers import pet_name_query as handler
from world_server.packets import pet_name_query as packet


def test_handle_pet_name_query(mocker, fake_db):
    mock_session = mocker.MagicMock()

    base_unit = game.UnitTemplate.get(Name='Young Nightsaber')
    world.Pet(
        id=10,
        base_unit=base_unit,
        name='Kiko',
        level=1,
        race=constants.ChrRaces[1],
        class_=constants.ChrClasses[base_unit.UnitClass],
        gender=enums.Gender.FEMALE,
        team=enums.Team.ALLIANCE,
        x=0,
        y=0,
        z=0,
        o=0,
        base_health=100,
        base_power=100,
    )

    client_pkt = packet.ClientPetNameQuery.parse(
        packet.ClientPetNameQuery.build(dict(pet_number=10, pet_guid=10)))

    response_pkts = handler.handle_pet_name_query(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerPetNameQuery.parse(response_bytes)
    assert response_op == op_code.Server.PET_NAME_QUERY
    assert response_pkt.number == 10
    assert response_pkt.name == 'Kiko'


def test_handle_pet_name_query_no_pet(mocker, fake_db):
    mock_session = mocker.MagicMock()

    client_pkt = packet.ClientPetNameQuery.parse(
        packet.ClientPetNameQuery.build(dict(pet_number=10, pet_guid=10)))

    response_pkts = handler.handle_pet_name_query(client_pkt, mock_session)

    assert len(response_pkts) == 0


if __name__ == '__main__':
    sys.exit(pytest.main([__file__]))
