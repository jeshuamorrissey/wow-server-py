from world_server.handlers import update_account_data as handler
from world_server.packets import update_account_data as packet


def test_handle_update_account_data():
    client_pkt = packet.ClientUpdateAccountData.parse(packet.ClientUpdateAccountData.build(dict(data=b'')))
    response_pkts = handler.handle_update_account_data(client_pkt, None)
    assert len(response_pkts) == 0
