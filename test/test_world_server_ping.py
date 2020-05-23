import enum
import sys

import pytest

from world_server import op_code
from world_server.handlers import ping as handler
from world_server.packets import ping as packet
from world_server.packets import pong


def test_handle_move_time_skipped(mocker, fake_db):
    mock_session = mocker.MagicMock()

    client_pkt = packet.ClientPing.parse(
        packet.ClientPing.build(dict(ping=1, latency=2)))

    response_pkts = handler.handle_ping(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_pkt_data = response_pkts[0]
    assert response_op == op_code.Server.PONG

    response_pkt = pong.ServerPong.parse(response_pkt_data)
    assert response_pkt.pong == 1
