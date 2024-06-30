import platform
import socket
import subprocess


def detect_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip


def ip_as_bytes(ip: str) -> bytes:
    return socket.inet_aton(ip)


def bytes_as_ip(bytes_: bytes) -> str:
    return socket.inet_ntoa(bytes_)


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.

    https://stackoverflow.com/questions/2953462/pinging-servers-in-python
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command) == 0
