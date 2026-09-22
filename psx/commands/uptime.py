from psx.utils.display import header, sep


def format_uptime(seconds: float) -> str:
    total_seconds = int(seconds)
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60

    parts = []

    if days > 0:
        parts.append(f"{days}d")
    if hours > 0 or days > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or not parts:
        parts.append(f"{minutes}m")

    return " ".join(parts) if parts else "0m"


def get_system_uptime() -> str:
    try:
        with open("/proc/uptime", "r", encoding="utf-8") as handle:
            seconds = float(handle.read().split()[0])
        return format_uptime(seconds)
    except OSError:
        return "Unknown"


def run() -> None:
    uptime = get_system_uptime()
    length = header("PsX Uptime")
    print(f"Uptime: {uptime}")
    sep(length)