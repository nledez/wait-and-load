from wait_and_load import WaitAndLoad

import pytest
import requests

from unittest.mock import call, patch, Mock


def catlog_nodes_empty():
    return "[]"


def connection_error():
    raise requests.exceptions.ConnectionError()


@patch(
    "consulate.Consul", **{"return_value.catalog.nodes.side_effect": catlog_nodes_empty}
)
def test_consul_status_ok(mock_nodes):
    wc = WaitAndLoad()
    assert wc.consul.status() is True


@patch(
    "consulate.Consul", **{"return_value.catalog.nodes.side_effect": connection_error}
)
def test_consul_status_ko(mock_nodes):
    wc = WaitAndLoad()
    assert wc.consul.status() is False


@patch("time.sleep", return_value=None)
@patch(
    "consulate.Consul", **{"return_value.catalog.nodes.side_effect": connection_error}
)
def test_consul_wait_ko(mock_nodes, mock_sleep):
    wc = WaitAndLoad(sleep_time=10, wait_count=5)
    assert wc.consul.wait() is False
    calls = [
        call(10),
        call(10),
        call(10),
        call(10),
        call(10),
    ]
    assert mock_sleep.call_count == len(calls)
    mock_sleep.assert_has_calls(calls)


CONSUL_CALLS = 0
CONSUL_CALL_MAX = 0


def one_consul_call():
    global CONSUL_CALLS, CONSUL_CALL_MAX
    CONSUL_CALLS += 1
    if CONSUL_CALLS >= CONSUL_CALL_MAX:
        return catlog_nodes_empty()
    else:
        return connection_error()


@patch("time.sleep", return_value=None)
@patch(
    "consulate.Consul", **{"return_value.catalog.nodes.side_effect": one_consul_call}
)
def test_consul_wait_ok(mock_nodes, mock_sleep):
    global CONSUL_CALLS, CONSUL_CALL_MAX

    CONSUL_CALLS = 0
    CONSUL_CALL_MAX = 3

    wc = WaitAndLoad(sleep_time=42, wait_count=20)
    assert wc.consul.wait() is True
    calls = [
        call(42),
        call(42),
        call(42),
    ]
    assert mock_sleep.call_count == len(calls)
    mock_sleep.assert_has_calls(calls)


@patch("consulate.Consul.kv", **{"__setitem__.side_effect": Mock()})
def test_consul_put_kv_ok(mock_kv):
    wc = WaitAndLoad()
    wc.consul.kv_put("dir/key", "value")

    calls = [call.__setitem__("dir/key", "value")]
    mock_kv.assert_has_calls(calls)


SET_SWITCH = 0


def set_item(key, value):
    global SET_SWITCH
    if SET_SWITCH == 0:
        SET_SWITCH = 1
        print("With exception")
        raise AttributeError()
    else:
        SET_SWITCH = 0
        print("Normal insert")


@patch(
    "consulate.Consul.kv",
    **{"__setitem__.side_effect": set_item, "__delitem__.side_effect": Mock()}
)
def test_consul_put_kv_ko(mock_kv):
    global SET_SWITCH
    SET_SWITCH = 0
    wc = WaitAndLoad()
    wc.consul.kv_put("dir/key", "value")

    calls = [
        call.__setitem__("dir/key", "value"),
        call.__delitem__("dir/key"),
        call.__setitem__("dir/key", "value"),
    ]
    assert len(mock_kv.mock_calls) == len(calls)
    mock_kv.assert_has_calls(calls)
