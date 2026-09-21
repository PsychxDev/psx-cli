import socket
import struct

import psutil

from psx.utils.display import header, sep


def _format_bytes(value: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    size = float(value)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"


def _get_default_gateway() -> str:
    try:
        with open("/proc/net/route", "r", encoding="utf-8") as handle:
            next(handle, None)
            for line in handle:
                fields = line.strip().split()
                if len(fields) >= 3 and fields[1] == "00000000":
                    gateway_hex = fields[2]
                    gateway = socket.inet_ntoa(struct.pack("<L", int(gateway_hex, 16)))
                    return gateway
        return "Not available"
    except Exception:
        return "Not available"


def _get_dns_servers() -> str:
    try:
        import os

        resolv_path = "/etc/resolv.conf"
        if not os.path.exists(resolv_path):
            return "Not available"

        servers = []
        with open(resolv_path, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line.startswith("nameserver"):
                    parts = line.split()
                    if len(parts) >= 2:
                        servers.append(parts[1])

        return ", ".join(servers) if servers else "Not available"
    except Exception:
        return "Not available"


def run() :
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)

    length = header("Network Information")

    for interface, addresses in interfaces.items():
        if interface == "lo":
            continue

        if interface not in stats or not stats[interface].isup:
            continue

        print(f"{'Interface:':12} {interface}")
        print(f"{'Status:':12} UP" if stats[interface].isup else f"{'Status:':12} DOWN")

        ipv4 = []
        ipv6 = []
        mac = "Not available"

        for address in addresses:
            if address.family == socket.AF_INET:
                ipv4.append(address.address)
            elif address.family == socket.AF_INET6:
                ipv6.append(address.address)
            elif address.family == socket.AF_PACKET and address.address:
                mac = address.address

        if ipv4:
            print(f"{'IPv4:':12} {', '.join(ipv4)}")
        if ipv6:
            print(f"{'IPv6:':12} {', '.join(ipv6)}")

        print(f"{'MAC:':12} {mac}")
        print(f"{'Gateway:':12} {_get_default_gateway()}")
        print(f"{'DNS:':12} {_get_dns_servers()}")

        counters = io_counters.get(interface)
        if counters:
            print(f"{'RX:':12} {_format_bytes(counters.bytes_recv)}")
            print(f"{'TX:':12} {_format_bytes(counters.bytes_sent)}")

    sep(length)