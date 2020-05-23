import enum
import sys
from unittest import mock

import pytest

from world_server import op_code
from world_server.handlers import gm_get_ticket as handler
from world_server.packets import gm_get_ticket as packet


def test_handle_gm_get_ticket(mocker, fake_db):
    mock_session = mock.MagicMock()

    client_pkt = packet.ClientGmGetTicket.parse(
        packet.ClientGmGetTicket.build(dict()))

    response_pkts = handler.handler(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = packet.ServerGmGetTicket.parse(response_bytes)
    assert response_op == op_code.Server.GM_GET_TICKET
    assert response_pkt.status == 0xA0
    assert response_pkt.ticket is None
