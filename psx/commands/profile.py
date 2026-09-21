import os
import platform
import socket

import psutil

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


def get_network_snapshot() -> list[dict]:
    snapshot = []
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for name, addrs in interfaces.items():
        if name == "lo":
            continue
        if name not in stats or not stats[name].isup:
            continue

        data = {"interface": name, "status": "UP", "ipv4": [], "ipv6": []}
        for addr in addrs:
            if addr.family == socket.AF_INET:
                data["ipv4"].append(addr.address)
            elif addr.family == socket.AF_INET6:
                data["ipv6"].append(addr.address)
        snapshot.append(data)

    return snapshot


def get_system_uptime() -> str:
    try:
        with open("/proc/uptime", "r", encoding="utf-8") as handle:
            seconds = float(handle.read().split()[0])
        return format_uptime(seconds)
    except Exception:
        return "Unknown"


def collect_profile() -> dict:
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "distro": platform.freedesktop_os_release().get("PRETTY_NAME", "Unknown"),
        "kernel": platform.release(),
        "uptime": get_system_uptime(),
        "memory": {
            "total": round(memory.total / (1024 ** 3), 2),
            "used": round(memory.used / (1024 ** 3), 2),
            "available": round(memory.available / (1024 ** 3), 2),
        },
        "disk": {
            "total": round(disk.total / (1024 ** 3), 2),
            "used": round(disk.used / (1024 ** 3), 2),
            "free": round(disk.free / (1024 ** 3), 2),
        },
        "network": get_network_snapshot(),
    }


def render_profile(profile: dict) -> None:
    print(f"{'Host:':12} {profile['hostname']}")
    print(f"{'OS:':12} {profile['os']}")
    print(f"{'Distro:':12} {profile['distro']}")
    print(f"{'Kernel:':12} {profile['kernel']}")
    print(f"{'Uptime:':12} {profile['uptime']}")
    print(f"{'RAM:':12} {profile['memory']['used']} GB / {profile['memory']['total']} GB")
    print(f"{'Disk:':12} {profile['disk']['used']} GB / {profile['disk']['total']} GB")

    print("Network")
    if profile["network"]:
        for item in profile["network"]:
            ipv4 = ", ".join(item["ipv4"]) if item["ipv4"] else "Not available"
            ipv6 = ", ".join(item["ipv6"]) if item["ipv6"] else "Not available"
            print(f"  {item['interface']:<8} {item['status']} | IPv4: {ipv4} | IPv6: {ipv6}")
    else:
        print("  No active interfaces found.")


def run() -> None:
    length = header("Profile")
    render_profile(collect_profile())
    sep(length)


def quick() -> None:
    profile = collect_profile()
    length = header("Quick")
    print(f"{'Host:':10} {profile['hostname']}")
    print(f"{'OS:':10} {profile['os']}")
    print(f"{'Kernel:':10} {profile['kernel']}")
    print(f"{'Uptime:':10} {profile['uptime']}")
    print(f"{'RAM:':10} {profile['memory']['used']} GB / {profile['memory']['total']} GB")
    print(f"{'Disk:':10} {profile['disk']['used']} GB / {profile['disk']['total']} GB")
    if profile["network"]:
        first = profile["network"][0]
        print(f"{'Network:':10} {first['interface']} ({', '.join(first['ipv4']) if first['ipv4'] else 'No IPv4'})")
    sep(length)
