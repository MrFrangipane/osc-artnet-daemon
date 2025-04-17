# https://stackoverflow.com/questions/2953462/pinging-servers-in-python
import platform
import subprocess


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    if platform.system().lower() == 'windows':
        return subprocess.call(['ping', '-n', '1', "-w", "500", host]) == 0

    return subprocess.call(['ping', '-c', '1', host]) == 0
