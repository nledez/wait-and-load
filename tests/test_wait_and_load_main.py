import os

from wait_and_load.__main__ import main

from unittest.mock import patch, Mock


@patch("wait_and_load.WaitAndLoad.Consul._consulate", **{"side_effect": Mock()})
@patch("wait_and_load.WaitAndLoad.Consul.wait", **{"side_effect": Mock()})
@patch("wait_and_load.WaitAndLoad.Consul.load", **{"side_effect": Mock()})
def test_main(mock_load, mock_wait, mock_consul):
    main()
    mock_consul.assert_called_once_with("http", "127.0.0.1", "8500")
    mock_wait.assert_called_once()
    mock_load.assert_not_called()

    mock_consul.reset_mock()
    mock_wait.reset_mock()
    mock_load.reset_mock()
    with patch.dict(os.environ, {"CONSUL_HTTP_ADDR": "https://consul:8501"}):
        main()
        mock_consul.assert_called_once_with("https", "consul", "8501")
        mock_wait.assert_called_once()
        mock_load.assert_not_called()

    mock_consul.reset_mock()
    mock_wait.reset_mock()
    mock_load.reset_mock()
    with patch.dict(os.environ, {"CONSUL_LOAD_FROM": "/data.yml"}):
        main()
        mock_consul.assert_called_once_with("http", "127.0.0.1", "8500")
        mock_wait.assert_called_once()
        mock_load.assert_called_once_with("/data.yml")
