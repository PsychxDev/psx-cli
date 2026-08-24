import psutil
import socket
from psx.utils.display import header, sep

def run() :
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for interface, addresses in interfaces.items():
        
        if interface == "lo" :
            continue

        if not stats[interface].isup :
            continue

        length = header("Network Information")
        
        print(f"{'Interface:':12} {interface}")
        print(f"{'Status:':12} UP" if stats[interface].isup else f"{'Status:':12} DOWN")
        
        for address in addresses :
            if address.family == socket.AF_INET :
                print(f"{'IPv4:':12} {address.address}")
                print(f"{'Netmask:':12} {address.netmask}")

        sep(length)