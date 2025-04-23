# https://stackoverflow.com/questions/2953462/pinging-servers-in-python
import platform
import subprocess


def ping(host: str, timeout: float=.5):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    if platform.system().lower() == 'windows':
        timeout = str(int(timeout * 1000))
        return subprocess.call(['ping', '-n', '1', "-w", timeout, host]) == 0

    timeout = str(timeout)
    return subprocess.call(['timeout', timeout, 'ping', '-c', '1', host]) == 0
