import psutil

from psx.commands.profile import collect_profile
from psx.utils.display import header, sep


def run() -> None:
    profile = collect_profile()
    length = header("Health")

    cpu_percent = psutil.cpu_percent(interval=None)

    ram_used = profile["memory"]["used"]
    ram_total = profile["memory"]["total"]
    ram_percent = (ram_used / ram_total * 100) if ram_total else 0

    disk_used = profile["disk"]["used"]
    disk_total = profile["disk"]["total"]
    disk_percent = (disk_used / disk_total * 100) if disk_total else 0

    issues = []
    if cpu_percent > 85:
        issues.append("CPU usage is high")
    if ram_percent > 80:
        issues.append("memory usage is high")
    if disk_percent > 85:
        issues.append("storage is nearly full")

    print(f"{'Processor:':12} {cpu_percent:.0f}% used")
    print(f"{'Memory:':12} {ram_percent:.0f}% used")
    print(f"{'Storage:':12} {disk_percent:.0f}% used")

    try:
        temps = psutil.sensors_temperatures()
        for entries in temps.values():
            if entries:
                print(f"{'Temperature:':12} {entries[0].current:.1f}C")
                break
        else:
            print(f"{'Temperature:':12} unavailable")
    except (AttributeError, OSError):
        print(f"{'Temperature:':12} unavailable")

    if profile["network"]:
        print(f"{'Internet:':12} Connected")
    else:
        issues.append("no network connection detected")

    if issues:
        print(f"{'Summary:':12} Needs attention: {'; '.join(issues)}.")
    else:
        print(f"{'Summary:':12} Your PC is healthy.")

    sep(length)
