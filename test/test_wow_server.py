import sys

from pony import orm


def test_wow_server_basic(mocker, fake_db):
    mock_thread = mocker.MagicMock()
    mock_thread_constructor = mocker.patch('threading.Thread', return_value=mock_thread)
    mocker.patch('coloredlogs.install')

    sys.argv = ['wow_server.py', '--auth_port', '1000', '--world_port', '1001', '--host', 'host']

    orm.db_session.__exit__()

    import wow_server
    mocker.patch.object(wow_server, '__name__', '__main__')
    wow_server.wow_server()

    assert mock_thread_constructor.call_count > 0
    assert mock_thread.start.call_count == mock_thread_constructor.call_count
    assert mock_thread.start.call_count == mock_thread.join.call_count

    # Required so post-test doesn't fail.
    orm.db_session.__enter__()
