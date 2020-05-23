from unittest import mock

from database import game
from world_server import op_code
from world_server.handlers import item_query_single as handler
from world_server.packets import item_query_single as packet


def test_handle_item_query_single(mocker, fake_db):
    mock_session = mock.MagicMock()

    item = game.ItemTemplate.get(entry=11922)

    client_pkt = packet.ClientItemQuerySingle.parse(packet.ClientItemQuerySingle.build(dict(
        entry=item.entry,
        guid=0,
    )))

    response_pkts = handler.handle_item_query_single(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerItemQuerySingle.parse(response_bytes)
    assert response_op == op_code.Server.ITEM_QUERY_SINGLE_RESPONSE
    assert response_pkt.entry == item.entry
