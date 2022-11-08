import consulate
import requests

class WaitAndLoad():
    def __init__(self):
        self.consul = self.Consul()

    class Consul():
        def __init__(self):
            self.consul = consulate.Consul()

        def status(self):
            try:
                self.consul.catalog.nodes()
                return True
            except requests.exceptions.ConnectionError:
                return False
