import subprocess
import platform
import re
from typing import List
from traceroute.settings import SETTINGS


def traceroute_subprocess(host: str, max_hops: int) -> List[str]:
    """
    Perform a system traceroute to the target host.
    Returns a list of hop IPs or '*' for unreachable hops.
    Raises ValueError if the traceroute command fails.
    """
    system = platform.system()
    try:
        if system == "Windows":
            cmd = ["tracert", "-h", str(max_hops), "/w", str(int(SETTINGS.DEFAULT_TIMEOUT * 1000)), host]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        else:
            cmd = ["traceroute", "-m", str(max_hops), "-n", host, "-w", str(int(SETTINGS.DEFAULT_TIMEOUT))]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=SETTINGS.DEFAULT_TIMEOUT * max_hops)
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Traceroute command failed: {e}")

    hops = []
    for line in result.stdout.splitlines():
        match = re.search(r"(\d{1,3}\.){3}\d{1,3}", line)
        if match:
            hops.append(match.group(0))
        elif "*" in line:
            hops.append("*")
    return hops
