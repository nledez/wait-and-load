import os

from . import WaitAndLoad


def main():
    API_HOST = os.environ.get("CONSUL_HTTP_ADDR", "http://127.0.0.1:8500")
    CONSUL_DATA = os.environ.get("CONSUL_LOAD_FROM", False)

    wc = WaitAndLoad(consul_addr=API_HOST)

    print("Wait Consul")
    wc.consul.wait()

    if CONSUL_DATA:
        print("Load data")
        wc.consul.load(CONSUL_DATA)


if __name__ == "__main__":  # pragma: nocover
    main()
