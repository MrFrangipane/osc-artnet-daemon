# https://stackoverflow.com/questions/2953462/pinging-servers-in-python
# https://stackoverflow.com/questions/4996852/how-to-just-call-a-command-and-not-get-its-output
# https://serverfault.com/questions/200468/how-can-i-set-a-short-timeout-with-the-ping-command
import platform
import subprocess


def ping(host: str, timeout: float=.5):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    if platform.system().lower() == 'windows':
        timeout = str(int(timeout * 1000))
        command = ['ping', '-n', '1', "-w", timeout, host]
    else:
        command = ['timeout', str(timeout), 'ping', '-c', '1', host]

    return subprocess.call(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ) == 0
