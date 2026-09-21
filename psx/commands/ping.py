import subprocess
import sys

from psx.utils.display import header, sep


def ping_host(host: str, count: int = 1) -> dict:
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), host],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return {
            "host": host,
            "reachable": False,
            "latency": "N/A",
            "status": "ping-unavailable",
            "detail": "ping command not available",
        }

    output = (result.stdout or "") + (result.stderr or "")
    latency = "N/A"
    for line in output.splitlines():
        if "time=" in line and "ms" in line:
            latency = line.split("time=")[-1].split()[0]
            break

    reachable = result.returncode == 0 and "time=" in output
    return {
        "host": host,
        "reachable": reachable,
        "latency": latency,
        "status": "reachable" if reachable else "unreachable",
        "detail": output.strip() or "Host did not respond.",
    }


def run(target: str = None) -> None:
    host = target or (sys.argv[2] if len(sys.argv) > 2 else None)
    length = header("Ping")

    if not host:
        print("Usage: psx ping <host>")
        sep(length)
        return

    result = ping_host(host)
    print(f"{'Host:':8} {result['host']}")
    print(f"{'Status:':8} {'OK' if result['reachable'] else 'DOWN'}")
    print(f"{'Latency:':8} {result['latency']}")

    if not result["reachable"]:
        print(f"{'Detail:':8} {result['detail']}")

    sep(length)
