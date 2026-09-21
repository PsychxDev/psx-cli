import time
import sys

import psutil

REFRESH_SECONDS = 1.5


def format_bytes(value: int) -> str:
    units = ("B", "KB", "MB", "GB", "TB")
    amount = float(value)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            return f"{amount:.1f} {unit}"
        amount /= 1024
    return "0.0 B"


def enter_live_screen() -> None:
    sys.stdout.write("\033[?1049h\033[?25l")
    sys.stdout.flush()


def leave_live_screen() -> None:
    sys.stdout.write("\033[?25h\033[?1049l")
    sys.stdout.flush()


def temperature() -> str:
    try:
        for entries in psutil.sensors_temperatures().values():
            if entries:
                return f"{entries[0].current:.1f}C"
    except (AttributeError, OSError):
        pass
    return "unavailable"


def collect_snapshot(previous: tuple[int, int] | None = None) -> dict:
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    counters = psutil.net_io_counters()
    current = (counters.bytes_sent, counters.bytes_recv)

    if previous is None:
        sent = received = 0
    else:
        sent = max(0, current[0] - previous[0])
        received = max(0, current[1] - previous[1])

    cpu = psutil.cpu_percent(interval=0.2)
    issues = []
    if cpu > 85:
        issues.append("processor is busy")
    if memory.percent > 80:
        issues.append("memory is high")
    if disk.percent > 85:
        issues.append("storage is nearly full")

    return {
        "cpu": cpu,
        "memory": memory.percent,
        "disk": disk.percent,
        "temperature": temperature(),
        "sent": sent,
        "received": received,
        "status": "Needs attention" if issues else "Healthy",
        "issues": issues,
        "network": current,
    }


def render(snapshot: dict, first_frame: bool = True) -> None:
    title = "===== PsX Track ====="
    lines = [
        title,
        "Live system monitor | refreshes every 1.5 seconds",
        "",
        f"{'Processor:':12} {snapshot['cpu']:.0f}% used",
        f"{'Memory:':12} {snapshot['memory']:.0f}% used",
        f"{'Storage:':12} {snapshot['disk']:.0f}% used",
        f"{'Temperature:':12} {snapshot['temperature']}",
        f"{'Network:':12} +{format_bytes(snapshot['sent'])} sent / {format_bytes(snapshot['received'])} received",
        f"{'Status:':12} {snapshot['status']}",
    ]

    if snapshot["issues"]:
        lines.append(f"{'Summary:':12} {'; '.join(snapshot['issues']).capitalize()}.")
    else:
        lines.append(f"{'Summary:':12} Your PC is healthy.")
    if first_frame:
        lines.extend(["", "Press Ctrl+C to stop."])
    lines.append("=" * len(title))
    sys.stdout.write("\033[2J\033[H" + "\n".join(lines) + "\n")
    sys.stdout.flush()


def run(action: str | None = None) -> None:
    previous = None
    first_frame = True
    once = action in {"--once", "once"}

    live_screen = not once
    if live_screen:
        enter_live_screen()

    try:
        while True:
            snapshot = collect_snapshot(previous)
            render(snapshot, first_frame)
            previous = snapshot["network"]
            first_frame = False
            if once:
                break
            time.sleep(REFRESH_SECONDS)
    except KeyboardInterrupt:
        pass
    finally:
        if live_screen:
            leave_live_screen()
            print("Track stopped.")
