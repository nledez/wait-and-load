import consulate
import requests
import time
import yaml


class WaitAndLoad:
    def __init__(
        self, consul_addr="http://127.0.0.1:8500", sleep_time=1, wait_count=60
    ):
        self.consul = self.Consul(consul_addr, sleep_time, wait_count)

    class Consul:
        def __init__(self, consul_addr, sleep_time, wait_count):
            try:
                (scheme, host, port) = consul_addr.replace("/", "").split(":")
            except ValueError:
                scheme = "http"
                (host, port) = consul_addr.split(":")
            self._scheme = scheme
            self._host = host
            self._port = port
            self.consul = self._consulate(scheme, host, port)
            self.sleep_time = sleep_time
            self.wait_count = wait_count

        @property
        def scheme(self):
            return self._scheme

        @property
        def host(self):
            return self._host

        @property
        def port(self):
            return self._port

        def _consulate(self, scheme, host, port):
            return consulate.Consul(scheme=scheme, host=host, port=port)

        def status(self):
            try:
                nodes = self.consul.catalog.nodes()
                print(f"Nodes: {nodes}")
                return True
            except requests.exceptions.ConnectionError:
                print("Can't get nodes")
                return False

        def wait(self):
            for _ in range(self.wait_count):
                time.sleep(self.sleep_time)
                print(".")
                if self.status():
                    return True
            return False

        def kv_put(self, key, value):
            try:
                print(f"Put: {key} => {value}")
                self.consul.kv[key] = value
            except AttributeError:
                del self.consul.kv[key]
                self.consul.kv[key] = value

        def load(self, filepath):
            with open(filepath, "r") as content:
                to_load = yaml.safe_load(content)
            for k, v in to_load.items():
                self.kv_put(k, v)
