# Module name : main.py
# created by alvifsandanamahardika at 6/10/21
import signal
import sys

from webserver import WebServer


def shutdownServer(sig, unused):
    """
    Shutdown server from a SIGINT received signal
    :param sig: integer
    """
    server.shutdown()
    sys.exit(1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, shutdownServer)
    server = WebServer(8000)
    server.start()
    print("Press Ctrl+C to shut down server.")
