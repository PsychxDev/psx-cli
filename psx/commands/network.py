import socket

import psutil
from psx.utils.display import header, sep


def run():
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    active = False
    length = header("Network Information")

    for interface, addresses in interfaces.items():
        if interface == "lo":
            continue

        if interface not in stats or not stats[interface].isup:
            continue

        active = True
        print(f"{'Interface:':12} {interface}")
        print(f"{'Status:':12} UP")

        for address in addresses:
            if address.family == socket.AF_INET:
                print(f"{'IPv4:':12} {address.address}")
                print(f"{'Netmask:':12} {address.netmask}")

        sep(length)

    if not active:
        print(f"{'Status:':12} OFFLINE")
        print(f"{'Message:':12} No active network interface detected.")
        sep(length)