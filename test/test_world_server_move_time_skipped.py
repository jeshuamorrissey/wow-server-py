import enum
import sys

import pytest

from world_server import op_code
from world_server.handlers import move_time_skipped as handler
from world_server.packets import move_time_skipped as packet


def test_handle_move_time_skipped(mocker, fake_db):
    mock_session = mocker.MagicMock()

    client_pkt = packet.ClientMoveTimeSkipped.parse(
        packet.ClientMoveTimeSkipped.build(dict(guid=1, time_skipped=2)))

    response_pkts = handler.handler(client_pkt, mock_session)

    assert len(response_pkts) == 0


if __name__ == '__main__':
    sys.exit(pytest.main([__file__]))
