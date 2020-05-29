import sys

from world_server import op_code
from world_server.handlers import query_time as handler
from world_server.packets import query_time as packet


def test_handle_query_time(mocker):
    mocker.patch('time.time', return_value=10)

    client_pkt = packet.ClientQueryTime.parse(packet.ClientQueryTime.build(dict()))

    response_pkts = handler.handle_query_time(client_pkt, mocker.MagicMock())

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerQueryTimeResponse.parse(response_bytes)
    assert response_op == op_code.Server.QUERY_TIME_RESPONSE
    assert response_pkt.time == 10
