import sys

import pytest

from database import enums
from world_server import op_code
from world_server.handlers import meetingstone_info as handler
from world_server.packets import meetingstone_info as packet
from world_server.packets import meetingstone_setqueue


def test_handle_meetingstone_info(mocker, fake_db):
    mock_session = mocker.MagicMock()

    client_pkt = packet.ClientMeetingstoneInfo.parse(
        packet.ClientMeetingstoneInfo.build(dict()))

    response_pkts = handler.handle_meetingstone_info(client_pkt, mock_session)

    assert len(response_pkts) == 1

    response_op, response_bytes = response_pkts[0]
    response_pkt = meetingstone_setqueue.ServerMeetingstoneSetqueue.parse(
        response_bytes)
    assert response_op == op_code.Server.MEETINGSTONE_SETQUEUE
    assert response_pkt.area_id == 0
    assert response_pkt.status == enums.MeetingStoneQueueStatus.NONE
