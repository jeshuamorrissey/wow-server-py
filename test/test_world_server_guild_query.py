from unittest import mock

from database import world
from world_server import op_code
from world_server.handlers import guild_query as handler
from world_server.packets import guild_query as packet


def test_handle_guild_query(mocker, fake_db):
    mock_session = mock.MagicMock()

    guild = world.Guild(
        id=1,
        name='name',
        emblem_style=2,
        emblem_color=3,
        border_style=4,
        border_color=5,
        background_color=6,
    )

    world.GuildRank(guild=guild, slot=0, name='Rank 0')
    world.GuildRank(guild=guild, slot=1, name='Rank 1')
    world.GuildRank(guild=guild, slot=2, name='Rank 2')

    client_pkt = packet.ClientGuildQuery.parse(packet.ClientGuildQuery.build(dict(id=1)))

    response_pkts = handler.handle_guild_query(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerGuildQuery.parse(response_bytes)
    assert response_op == op_code.Server.GUILD_QUERY_RESPONSE
    assert response_pkt.id == 1
    assert response_pkt.name == 'name'
    assert response_pkt.rank_names == ['Rank 0', 'Rank 1', 'Rank 2'] + [''] * 7
