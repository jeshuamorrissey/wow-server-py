from unittest import mock

from world_server import op_code
from world_server.handlers import battlefield_status as handler
from world_server.packets import battlefield_status as packet


def test_handle_battlefield_status(mocker, fake_db):
    mock_session = mock.MagicMock()

    client_pkt = packet.ClientBattlefieldStatus.parse(packet.ClientBattlefieldStatus.build(dict()))

    response_pkts = handler.handler(client_pkt, mock_session)

    assert len(response_pkts) == 3

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerBattlefieldStatus.parse(response_bytes)
    assert response_op == op_code.Server.BATTLEFIELD_STATUS
    assert response_pkt.queue_slot == 0
    assert response_pkt.data is None

    response_op, response_bytes = response_pkts[1]
    response_pkt = packet.ServerBattlefieldStatus.parse(response_bytes)
    assert response_op == op_code.Server.BATTLEFIELD_STATUS
    assert response_pkt.queue_slot == 1
    assert response_pkt.data is None

    response_op, response_bytes = response_pkts[2]
    response_pkt = packet.ServerBattlefieldStatus.parse(response_bytes)
    assert response_op == op_code.Server.BATTLEFIELD_STATUS
    assert response_pkt.queue_slot == 2
    assert response_pkt.data is None
