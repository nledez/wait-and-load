import consulate
import requests
import time


class WaitAndLoad:
    def __init__(self, sleep_time=1, wait_count=60):
        self.consul = self.Consul(sleep_time, wait_count)

    class Consul:
        def __init__(self, sleep_time, wait_count):
            self.consul = consulate.Consul()
            self.sleep_time = sleep_time
            self.wait_count = wait_count

        def status(self):
            try:
                self.consul.catalog.nodes()
                return True
            except requests.exceptions.ConnectionError:
                return False

        def wait(self):
            for _ in range(self.wait_count):
                time.sleep(self.sleep_time)
                if self.status():
                    return True
            return False

        def kv_put(self, key, value):
            try:
                self.consul.kv[key] = value
            except AttributeError:
                del self.consul.kv[key]
                self.consul.kv[key] = value
