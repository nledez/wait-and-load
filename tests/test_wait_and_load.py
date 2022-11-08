from wait_and_load import WaitAndLoad

import requests

from unittest.mock import patch


@patch('consulate.Consul', **{'return_value.catalog.nodes.return_value': '[]'})
def test_consul_status_ok(mock_nodes):
    wc = WaitAndLoad()
    assert wc.consul.status() is True


@patch('consulate.Consul',
       **{'return_value.catalog.nodes.side_effect':
          requests.exceptions.ConnectionError()})
def test_consul_status_ko(mock_nodes):
    wc = WaitAndLoad()
    assert wc.consul.status() is False
