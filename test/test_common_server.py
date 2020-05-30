from common import server


def test_server_run(mocker):
    mock_server_bind = mocker.patch('socketserver.TCPServer.server_bind')
    mock_server_activate = mocker.patch('socketserver.TCPServer.server_activate')
    mock_serve_forever = mocker.patch.object(server.Server, 'serve_forever')

    packet_formats = {1: 'format'}
    handlers = {2: 'handlers'}

    server.run(
        name='name',
        host='host',
        port=100,
        session_type=int,
        packet_formats=packet_formats,
        handlers=handlers,
    )

    mock_serve_forever.assert_called_once_with()
    mock_server_bind.assert_called_once_with()
    mock_server_activate.assert_called_once_with()
    assert server.Server.allow_reuse_address
